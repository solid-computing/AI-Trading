# AI Trading Bot - User Guide

**Version 1.0**  
**Last Updated: 2024**

---

## Table of Contents

1. [Introduction](#introduction)
2. [What is the AI Trading Bot?](#what-is-the-ai-trading-bot)
3. [Prerequisites](#prerequisites)
4. [Getting Started](#getting-started)
5. [Configuration](#configuration)
6. [Using the Bot](#using-the-bot)
7. [Monitoring Your Trades](#monitoring-your-trades)
8. [Managing the Bot](#managing-the-bot)
9. [Troubleshooting](#troubleshooting)
10. [Safety and Best Practices](#safety-and-best-practices)

---

## Introduction

Welcome to the AI Trading Bot User Guide! This document will help you understand how to use the automated cryptocurrency trading bot for Binance. Whether you're a beginner or an experienced trader, this guide provides step-by-step instructions to get you started safely.

### Important Disclaimer

**⚠️ Trading cryptocurrencies involves significant financial risk.** This bot is provided for educational purposes only. Always:

- Start with dry-run mode (simulated trading)
- Test with small amounts before scaling up
- Never invest more than you can afford to lose
- Monitor your bot regularly
- Understand the trading strategy being used

---

## What is the AI Trading Bot?

The AI Trading Bot is an automated cryptocurrency trading system that:

- **Trades 24/7**: Monitors markets and executes trades automatically
- **Uses Technical Analysis**: Makes decisions based on RSI, Moving Averages, MACD, and Volume indicators
- **Manages Risk**: Implements stop-loss orders and position sizing
- **Sends Notifications**: Alerts you via Telegram about trades and important events
- **Runs on Cloud**: Deploys to a VPS for uninterrupted operation

### Key Features

- **Exchange Support**: Binance Spot Trading
- **Trading Strategy**: RSI + Moving Average + MACD + Volume analysis
- **Notifications**: Real-time Telegram alerts
- **Deployment Options**: 
  - Local development (Docker)
  - Fully automated cloud deployment (Terraform + CircleCI)
  - Manual VPS deployment
- **Cost-Effective**: Runs on a small VPS (~€3-5/month)

---

## Prerequisites

Before you start, you'll need:

### 1. Accounts and Access

- **Binance Account**: For cryptocurrency trading
  - Account must be verified (KYC completed)
  - 2FA (Two-Factor Authentication) enabled recommended
  
- **Telegram Account**: For receiving notifications
  - Download Telegram app or use web version
  
- **Cloud Provider** (for production deployment):
  - OVH Cloud account (recommended, ~€3-5/month)
  - OR any VPS provider with Ubuntu support
  
- **CircleCI Account** (optional, for automated deployments):
  - Free tier available
  - Connected to your GitHub repository

### 2. Technical Requirements

For local testing:
- Computer with Docker installed
- Basic command-line knowledge
- Internet connection

For production deployment:
- SSH access to a VPS
- Basic Linux administration knowledge (helpful but not required)

### 3. Financial Preparation

- **Minimum Trading Capital**: €100-500 recommended for testing
- **VPS Costs**: €3-5/month for small instances
- **Time Investment**: 2-4 hours for initial setup

---

## Getting Started

### Step 1: Get Your API Keys

#### Binance API Setup

1. **Login to Binance** and go to [API Management](https://www.binance.com/en/my/settings/api-management)

2. **Create a New API Key**:
   - Click "Create API"
   - Label it "Trading Bot" (or your preferred name)
   - Complete security verification (email/SMS)

3. **Configure API Permissions**:
   - ✅ **Enable**: Spot & Margin Trading
   - ❌ **Disable**: Futures Trading (for safety)
   - ❌ **Disable**: Withdrawals (for security)
   
4. **Save Your Credentials** (you'll need these later):
   ```
   API Key: your_binance_api_key_here
   Secret Key: your_binance_secret_key_here
   ```

5. **Optional but Recommended**: Set IP restrictions
   - Add your VPS IP address (you'll get this after infrastructure setup)
   - Increases security significantly

#### Telegram Bot Setup

1. **Open Telegram** and search for `@BotFather`

2. **Create a New Bot**:
   - Send message: `/newbot`
   - Follow the prompts to choose a name and username
   - BotFather will give you a **token**

3. **Save Your Bot Token**:
   ```
   Bot Token: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

4. **Get Your Chat ID**:
   - Message your new bot (say "Hello")
   - Visit in browser: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Look for `"chat":{"id":` in the response
   - Save this number:
   ```
   Chat ID: 123456789
   ```

### Step 2: Choose Your Deployment Method

You have three options:

#### Option A: Fully Automated (Recommended for Beginners)

**What you do**:
- Configure CircleCI with your API keys
- Push code to GitHub

**What happens automatically**:
- Infrastructure is created on OVH Cloud
- VPS is configured
- Bot is deployed and started

**Best for**: Users who want a hands-off experience

#### Option B: Manual Infrastructure + Auto Deployment

**What you do**:
- Run Terraform commands to create infrastructure
- Configure CircleCI for deployments

**What happens automatically**:
- Application updates deploy automatically when you push code

**Best for**: Users who want control over infrastructure but automated deployments

#### Option C: Fully Manual (For Testing)

**What you do**:
- Set up everything manually
- Run bot locally on your computer

**What happens**:
- You control every aspect
- Good for learning and testing

**Best for**: Developers and those who want full control

### Step 3: Local Testing (Recommended First Step)

Before deploying to production, test locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/solid-computing/AI-Trading.git
   cd AI-Trading
   ```

2. **Create Environment File**:
   ```bash
   cp .env.example .env
   nano .env  # Or use any text editor
   ```

3. **Add Your API Keys** to `.env`:
   ```
   BINANCE_API_KEY=your_api_key_here
   BINANCE_API_SECRET=your_secret_here
   TELEGRAM_TOKEN=your_telegram_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

4. **Start in Dry-Run Mode** (no real trades):
   ```bash
   make quick-start
   ```

5. **Check the Logs**:
   ```bash
   make logs
   ```

6. **Verify Telegram Notifications**:
   - You should receive a startup message
   - Try sending `/status` to your bot

---

## Configuration

### Understanding Configuration Files

The bot uses JSON configuration files:

- **`config.dryrun.json`**: For testing without real money
- **`config.live.template.json`**: Template for live trading
- **`pairs.json`**: List of trading pairs (e.g., BTC/USDT, ETH/USDT)

### Trading Pairs

The bot trades cryptocurrency pairs. Default pairs are configured in `pairs.json`:

```json
{
  "pairs": [
    "BTC/USDT",
    "ETH/USDT",
    "BNB/USDT"
  ]
}
```

**To modify trading pairs**:
1. Edit `pairs.json`
2. Add or remove pairs as needed
3. Restart the bot

**Recommendations**:
- Start with 2-3 major pairs
- Avoid low-volume or exotic pairs
- More pairs = more opportunities but higher risk

### Risk Settings

Key risk parameters (in configuration file):

```json
{
  "max_open_trades": 3,
  "stake_amount": 100,
  "stake_currency": "USDT"
}
```

- **max_open_trades**: Maximum number of simultaneous trades (default: 3)
- **stake_amount**: Amount to invest per trade in USDT (default: 100)
- **stake_currency**: The currency to use for trading (usually USDT)

### Stop Loss and Take Profit

The bot automatically manages risk:

- **Stop Loss**: -5% (exits trade if it loses 5%)
- **ROI (Return on Investment) Targets**:
  - 0 minutes: 4% profit target
  - 20 minutes: 2% profit target
  - 60 minutes: 1% profit target

These are configured in the strategy file and can be adjusted.

---

## Using the Bot

### Starting the Bot

#### Dry-Run Mode (Testing)

Always start with dry-run mode:

```bash
# Local
make quick-start

# Or with docker-compose directly
docker-compose up -d
```

The bot will:
- Connect to Binance
- Analyze markets
- Simulate trades (no real money)
- Send Telegram notifications

#### Live Trading Mode

**⚠️ Only use after successful dry-run testing!**

1. **Switch to Live Configuration**:
   - Update your configuration to use live mode
   - Double-check all settings

2. **Start Live Trading**:
   ```bash
   # Ensure you're using live config
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Monitor Closely**:
   - Watch for the first few hours
   - Verify trades are executing correctly
   - Check Telegram notifications

### Telegram Commands

Once running, you can control the bot via Telegram:

- `/start` - Start receiving notifications
- `/status` - Get current bot status
- `/profit` - Show profit/loss summary
- `/balance` - Show account balance
- `/trades` - List open trades
- `/daily` - Daily profit summary
- `/stop` - Stop the bot (use with caution)

### Understanding Bot Behavior

The bot will:

1. **Analyze Markets** every few seconds
2. **Look for Entry Signals**:
   - RSI below 30 (oversold)
   - Price above moving average (uptrend)
   - Volume spike (increased interest)
   - MACD crossover (momentum)

3. **Execute Trades** when all conditions are met
4. **Monitor Open Positions** continuously
5. **Exit Trades** when:
   - Profit target is reached
   - Stop loss is triggered
   - Exit signal is detected (RSI > 70, price below MA)

---

## Monitoring Your Trades

### Telegram Notifications

You'll receive messages for:

- **Trade Entry**: "New trade: BUY BTC/USDT @ $45,000"
- **Trade Exit**: "Closed trade: SELL BTC/USDT @ $46,000 | Profit: 2.2%"
- **Errors**: "⚠️ API Error: Rate limit exceeded"
- **Daily Summaries**: End-of-day profit/loss reports

### Log Files

**Local Development**:
```bash
make logs
```

**Production VPS**:
```bash
ssh freqtrade@your-vps-ip
journalctl -u freqtrade -f
```

### What to Watch For

**Good Signs**:
- Regular market updates in logs
- Successful API connections
- Trades executing as expected
- Positive profit trends

**Warning Signs**:
- Repeated API errors
- No trades for extended periods (could indicate issue)
- Unexpected losses
- Bot not responding to commands

---

## Managing the Bot

### Checking Bot Status

**Local**:
```bash
make status
```

**VPS**:
```bash
sudo systemctl status freqtrade
```

### Stopping the Bot

**Local**:
```bash
make down
```

**VPS**:
```bash
sudo systemctl stop freqtrade
```

### Restarting the Bot

**Local**:
```bash
make down
make up
```

**VPS**:
```bash
sudo systemctl restart freqtrade
```

### Updating the Bot

**With CircleCI** (automated):
- Just push code to GitHub
- CircleCI will deploy automatically

**Manual Update**:
```bash
git pull origin main
make deploy
```

### Emergency Stop

If you need to stop trading immediately:

1. **Stop the Bot**:
   ```bash
   sudo systemctl stop freqtrade
   ```

2. **Cancel Open Orders** (if needed):
   ```bash
   docker exec freqtrade freqtrade cancel_open_orders
   ```

3. **Close Positions** (if desired):
   - Can be done manually on Binance
   - Or wait for bot to exit based on strategy

---

## Troubleshooting

### Common Issues and Solutions

#### Bot Won't Start

**Problem**: Bot fails to start or crashes immediately

**Solutions**:
1. Check API keys are correct in `.env` file
2. Verify Binance API has correct permissions
3. Check internet connectivity
4. Review logs for specific error messages

```bash
# Check logs
make logs
```

#### No Telegram Notifications

**Problem**: Not receiving messages from bot

**Solutions**:
1. Verify bot token is correct
2. Check chat ID is accurate
3. Make sure you've sent a message to the bot first
4. Test bot token: `https://api.telegram.org/bot<TOKEN>/getMe`

#### API Errors

**Problem**: "API Error" or "Rate limit exceeded"

**Solutions**:
1. Check Binance API key restrictions (IP whitelist)
2. Verify API permissions are correct
3. Wait a few minutes (rate limits reset)
4. Check Binance status page for outages

#### No Trades Executing

**Problem**: Bot running but not making any trades

**Possible Reasons**:
1. Market conditions don't meet entry criteria (normal)
2. Configuration issue (check max_open_trades)
3. Insufficient balance
4. Dry-run mode still active (check config)

**What to do**:
```bash
# Check balance
docker exec freqtrade freqtrade show_balance

# Verify configuration
cat config.dryrun.json | grep dry_run
```

#### Bot Making Too Many Trades

**Problem**: Excessive trading activity

**Solutions**:
1. Reduce max_open_trades in configuration
2. Adjust strategy parameters (more conservative)
3. Review trading pairs (remove volatile pairs)

### Getting Help

If you're still stuck:

1. **Check Documentation**:
   - README.md
   - SETUP.md
   - DEPLOYMENT_CHECKLIST.md

2. **Review Logs**: Often contain specific error messages

3. **Freqtrade Documentation**: https://www.freqtrade.io/

4. **Community Support**:
   - Freqtrade Discord: https://discord.gg/p7nuUNVfP7
   - GitHub Issues

---

## Safety and Best Practices

### Security

1. **Never Share API Keys**:
   - Keep them secure
   - Don't commit to Git
   - Use environment variables

2. **Enable 2FA**:
   - On Binance account
   - On GitHub account
   - On VPS if possible

3. **Use IP Restrictions**:
   - Whitelist only your VPS IP on Binance
   - Limit SSH access to known IPs

4. **Regular Monitoring**:
   - Check bot at least daily
   - Review trade performance
   - Monitor account balance

### Trading Best Practices

1. **Start Small**:
   - Begin with dry-run mode
   - Use small stake amounts initially
   - Gradually increase as you gain confidence

2. **Diversify**:
   - Don't put all capital in one pair
   - Use max_open_trades to limit exposure

3. **Monitor Performance**:
   - Track profit/loss daily
   - Adjust strategy if needed
   - Know when to stop

4. **Stay Informed**:
   - Understand market conditions
   - Be aware of major crypto news events
   - Know the limitations of automated trading

5. **Set Limits**:
   - Define maximum loss you're willing to accept
   - Set a budget for trading capital
   - Don't chase losses

### Maintenance

1. **Regular Updates**:
   - Keep bot software updated
   - Update dependencies periodically
   - Monitor for security patches

2. **Backup**:
   - Backup configuration files
   - Keep records of trades
   - Document your setup

3. **Testing**:
   - Test configuration changes in dry-run
   - Backtest strategy modifications
   - Monitor new pairs carefully

---

## Quick Reference

### Essential Commands

```bash
# Local Development
make validate          # Check setup
make quick-start      # Start bot in dry-run
make logs             # View logs
make down             # Stop bot
make status           # Check status

# VPS Management
sudo systemctl status freqtrade    # Check service
sudo systemctl restart freqtrade   # Restart
journalctl -u freqtrade -f         # View logs
```

### Key Configuration Files

- `.env` - Environment variables and API keys
- `config.dryrun.json` - Dry-run configuration
- `config.live.template.json` - Live trading template
- `pairs.json` - Trading pairs list

### Important Telegram Commands

- `/status` - Bot status
- `/profit` - Show profits
- `/balance` - Account balance
- `/trades` - Open trades

### Support Resources

- **Documentation**: https://www.freqtrade.io/
- **Community**: https://discord.gg/p7nuUNVfP7
- **GitHub**: Issues and discussions

---

## Conclusion

Congratulations! You now have a comprehensive understanding of how to use the AI Trading Bot. Remember:

- **Start with dry-run mode**
- **Monitor regularly**
- **Start small and scale gradually**
- **Never invest more than you can afford to lose**

Happy trading! 🚀📈

---

*Document Version: 1.0*  
*For the latest updates, check the GitHub repository.*
