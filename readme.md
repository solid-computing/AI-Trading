# Freqtrade Trading Bot

A comprehensive Freqtrade trading bot setup for automated cryptocurrency trading on Binance with Telegram notifications, Docker deployment, and CI/CD pipeline.

## Features

- **Exchange**: Binance (Spot Trading)  
- **Notifications**: Telegram integration
- **Strategy**: RsiMaStrategy (RSI + Moving Average)
- **Deployment**: Docker Compose for local development, systemd service for VPS
- **CI/CD**: CircleCI pipeline with automated testing and deployment
- **VPS**: Optimized for OVH VPS SSD 1 (1 vCPU, 2 GB RAM, 20 GB SSD)

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Trading
   ```

2. **Configure the bot**
   ```bash
   # Copy and edit configuration files
   cp config.dryrun.json config.local.json
   # Edit config.local.json with your API keys (for testing)
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Check logs**
   ```bash
   docker-compose logs -f freqtrade
   ```

### VPS Deployment

1. **Setup VPS** (Run once on new VPS)
   ```bash
   # Copy setup script to VPS and run
   scp deployment/setup-vps.sh user@your-vps:/tmp/
   ssh user@your-vps "chmod +x /tmp/setup-vps.sh && sudo /tmp/setup-vps.sh"
   ```

2. **Configure secrets**
   ```bash
   # On VPS, create .env file
   sudo cp /home/freqtrade/.env.template /home/freqtrade/.env
   sudo nano /home/freqtrade/.env  # Add your actual API keys
   ```

3. **Deploy** (Done automatically via CircleCI or manually)
   ```bash
   ./deployment/deploy.sh
   ```

## Configuration

### Configuration Files

- `config.dryrun.json` - Dry-run configuration for testing
- `config.live.template.json` - Live trading template (DO NOT put real API keys here)
- `pairs.json` - Trading pairs configuration

### Environment Variables (Secrets)

Set these in your CircleCI Context `freqtrade-secrets`:

```bash
# Binance API
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret

# Telegram Bot
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# VPS Access
OVH_SSH_KEY=base64_encoded_private_key
OVH_HOST=your.vps.ip
OVH_USER=freqtrade
OVH_SSH_FINGERPRINT=ssh_key_fingerprint
```

## Strategy: RsiMaStrategy

A simple starter strategy that combines:
- **RSI (Relative Strength Index)**: Identifies oversold/overbought conditions
- **Moving Average**: Confirms trend direction
- **Volume**: Ensures sufficient market activity
- **MACD**: Additional momentum confirmation
- **Bollinger Bands**: Volatility and price level analysis

### Entry Conditions
- RSI < 30 (oversold)
- Price > 20-period SMA (uptrend)
- Volume > 1.2x average volume
- MACD > Signal line
- Price below upper Bollinger Band

### Exit Conditions
- RSI > 70 (overbought)
- Price < 20-period SMA (downtrend)
- MACD < Signal line
- Price hits upper Bollinger Band

### Risk Management
- Stop Loss: -5%
- Take Profit: ROI table (4% immediate, 2% at 30min, 1% at 60min)
- Max open trades: 3

## Development

### Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run linting
black user_data/strategies/
flake8 user_data/strategies/

# Validate strategy
python -c "from user_data.strategies.RsiMaStrategy import RsiMaStrategy; print('Strategy valid')"

# Run backtest
freqtrade backtesting --config config.dryrun.json --strategy RsiMaStrategy
```

### Project Structure

```
AI-Trading/
├── .circleci/
│   └── config.yml              # CircleCI pipeline
├── deployment/
│   ├── deploy.sh               # Deployment script
│   ├── freqtrade.service       # Systemd service
│   └── setup-vps.sh            # VPS setup script
├── user_data/
│   └── strategies/
│       └── RsiMaStrategy.py    # Trading strategy
├── config.dryrun.json          # Dry-run config
├── config.live.template.json   # Live config template
├── pairs.json                  # Trading pairs
├── docker-compose.yml          # Local development
├── docker-compose.prod.yml     # Production deployment
├── Dockerfile                  # Docker image
├── requirements.txt            # Python dependencies
└── readme.md                   # This file
```

## CI/CD Pipeline

The CircleCI pipeline includes:

1. **Lint & Test**: Code quality checks and strategy validation
2. **Backtest**: Run backtests to validate strategy performance
3. **Build Docker**: Build and test Docker image
4. **Deploy**: Deploy to VPS (main branch only)

### Pipeline Stages

```yaml
lint-and-test → backtest → build-docker → deploy
                    ↓           ↓           ↓
                 Parallel   Parallel    Main only
```

## Monitoring

### Local Monitoring

- **Logs**: `docker-compose logs -f freqtrade`
- **FreqUI**: Access at http://localhost:8081 (if enabled)

### VPS Monitoring

- **Service Status**: `sudo systemctl status freqtrade`
- **Logs**: `journalctl -u freqtrade -f`
- **Docker Status**: `sudo docker ps`

### Telegram Notifications

The bot will send notifications for:
- Trade entries and exits
- Errors and warnings  
- Daily summaries
- System status

## Security Best Practices

1. **Never commit API keys** - Use environment variables and CircleCI Context
2. **Use dedicated API keys** with minimal permissions (Spot trading only)
3. **Enable 2FA** on all exchange and service accounts
4. **Regular monitoring** of trades and system health
5. **Start with small amounts** and dry-run testing

## Troubleshooting

### Common Issues

**Docker build fails**
```bash
# Clear Docker cache
docker system prune -a
docker-compose build --no-cache
```

**Strategy import errors**
```bash
# Check Python syntax
python -m py_compile user_data/strategies/RsiMaStrategy.py
```

**VPS deployment fails**
```bash
# Check SSH connectivity
ssh user@your-vps "echo 'SSH working'"

# Check service status
ssh user@your-vps "sudo systemctl status freqtrade"
```

**API connection errors**
- Verify API keys are correct
- Check IP whitelist on Binance
- Ensure sufficient permissions

### Logs

- **Local**: `docker-compose logs freqtrade`
- **VPS**: `journalctl -u freqtrade -f`
- **Freqtrade**: Check `user_data/logs/` directory

## Cost Estimation

### OVH VPS SSD 1
- **Specs**: 1 vCPU, 2 GB RAM, 20 GB SSD
- **Cost**: ~€3-€5/month
- **Performance**: Suitable for 1-3 trading pairs with 5m timeframe

### Additional Costs
- **Domain** (optional): ~€10/year
- **Monitoring** (optional): Various free/paid options

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test locally
4. Submit a pull request

## Disclaimer

⚠️ **Trading cryptocurrencies involves significant risk**. This bot is for educational purposes. Always:
- Test thoroughly with dry-run mode
- Start with small amounts
- Monitor performance closely
- Understand the risks involved
- Never invest more than you can afford to lose

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Documentation**: [Freqtrade Docs](https://www.freqtrade.io/)
- **Community**: [Freqtrade Discord](https://discord.gg/p7nuUNVfP7)
- **Issues**: Use GitHub Issues for bug reports and feature requests
