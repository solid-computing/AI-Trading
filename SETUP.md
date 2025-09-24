# Manual Setup Guide - AI Trading Bot

This guide provides step-by-step instructions for the manual configuration needed before deployment.

## Prerequisites

Before starting the setup, ensure you have:
- A VPS (OVH recommended, minimum 2GB RAM, 20GB SSD)
- Binance account with API access
- Telegram bot token
- CircleCI account
- Basic command line knowledge

## 🔐 1. API Keys & Credentials Setup

### 1.1 Binance API Keys

1. **Login to Binance**
   - Go to [Binance API Management](https://www.binance.com/en/my/settings/api-management)
   - Click "Create API"
   - Enter a label (e.g., "Trading Bot")

2. **Configure API Permissions**
   - ✅ Enable Spot & Margin Trading
   - ❌ Disable Futures Trading (for safety)
   - ❌ Disable Withdrawals (for security)
   - Set IP restrictions if using a fixed VPS IP

3. **Save Your Keys**
   ```
   BINANCE_API_KEY=your_actual_api_key_here
   BINANCE_API_SECRET=your_actual_secret_here
   ```

### 1.2 Telegram Bot Setup

1. **Create Telegram Bot**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot`
   - Choose a name and username for your bot
   - Save the bot token

2. **Get Your Chat ID**
   - Message your bot first
   - Go to: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

3. **Save Your Credentials**
   ```
   TELEGRAM_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

## 🖥️ 2. VPS Setup

### 2.1 Server Preparation

1. **Connect to your VPS**
   ```bash
   ssh root@your_vps_ip
   ```

2. **Run the setup script**
   ```bash
   # Clone the repository first
   git clone https://github.com/solid-computing/AI-Trading.git
   cd AI-Trading
   
   # Make setup script executable and run it
   chmod +x deployment/setup-vps.sh
   ./deployment/setup-vps.sh
   ```

3. **Configure environment variables**
   ```bash
   # Copy the template and edit it
   sudo cp /home/freqtrade/.env.template /home/freqtrade/.env
   sudo nano /home/freqtrade/.env
   
   # Add your actual credentials:
   BINANCE_API_KEY=your_actual_api_key_here
   BINANCE_API_SECRET=your_actual_secret_here
   TELEGRAM_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

4. **Set proper permissions**
   ```bash
   sudo chown freqtrade:freqtrade /home/freqtrade/.env
   sudo chmod 600 /home/freqtrade/.env
   ```

### 2.2 SSH Key Setup

1. **Generate SSH key for CircleCI**
   ```bash
   ssh-keygen -t rsa -b 4096 -C "circleci@yourdomain.com"
   # Save as: /home/yourusername/.ssh/id_rsa_circleci
   ```

2. **Add public key to VPS**
   ```bash
   # Copy public key to authorized_keys
   cat ~/.ssh/id_rsa_circleci.pub >> ~/.ssh/authorized_keys
   ```

3. **Get private key for CircleCI** (base64 encoded)
   ```bash
   base64 -w 0 ~/.ssh/id_rsa_circleci
   # Copy this output for CircleCI environment variables
   ```

## 🔄 3. CircleCI Configuration

### 3.1 Create Context

1. **Go to CircleCI**
   - Navigate to Organization Settings → Contexts
   - Click "Create Context"
   - Name it: `freqtrade-secrets`

### 3.2 Add Environment Variables

Add the following variables to the `freqtrade-secrets` context:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `BINANCE_API_KEY` | Your Binance API key | Trading API access |
| `BINANCE_API_SECRET` | Your Binance API secret | Trading API secret |
| `TELEGRAM_TOKEN` | Your Telegram bot token | Notifications |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | Notification target |
| `OVH_HOST` | Your VPS IP address | Deployment target |
| `OVH_USER` | VPS username (usually `root`) | SSH user |
| `OVH_SSH_KEY` | Base64 encoded private key | SSH authentication |
| `OVH_SSH_FINGERPRINT` | SSH key fingerprint | Key identification |

### 3.3 Get SSH Fingerprint

```bash
# On your local machine
ssh-keygen -lf ~/.ssh/id_rsa_circleci
# Copy the fingerprint (format: SHA256:xxxxx)
```

## 🧪 4. Local Testing

### 4.1 Environment Setup

1. **Create local environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Test configuration**
   ```bash
   make validate
   ```

### 4.2 Dry Run Testing

1. **Start in dry-run mode**
   ```bash
   make quick-start
   ```

2. **Check logs**
   ```bash
   make logs
   ```

3. **Verify bot status**
   ```bash
   make status
   ```

## 📋 5. Configuration Files

### 5.1 Trading Configuration

Edit these files as needed:

- **`config.dryrun.json`** - Local testing configuration
- **`config.live.template.json`** - Production template (uses environment variables)
- **`pairs.json`** - Trading pairs selection

### 5.2 Update Trading Pairs

```bash
# Update pairs configuration
make update-config
```

## 🚀 6. Deployment Process

### 6.1 Manual Deployment

```bash
# Deploy to VPS manually
export OVH_HOST=your_vps_ip
export OVH_USER=root
make deploy
```

### 6.2 Automatic Deployment

1. **Push to main branch**
   ```bash
   git add .
   git commit -m "Configure trading bot"
   git push origin main
   ```

2. **Monitor CircleCI**
   - Check the pipeline status
   - Verify deployment succeeded

3. **Verify on VPS**
   ```bash
   ssh root@your_vps_ip
   sudo systemctl status freqtrade
   journalctl -u freqtrade -f
   ```

## 🛠️ 7. Post-Deployment Verification

### 7.1 Service Status

```bash
# Check if service is running
sudo systemctl status freqtrade

# View logs
journalctl -u freqtrade -f

# Check Docker containers
sudo docker ps
```

### 7.2 Telegram Notifications

- Send `/status` command to your bot
- Verify you receive trading notifications
- Test with `/balance` and `/profit` commands

### 7.3 Monitor Trading

```bash
# View live logs
journalctl -u freqtrade -f

# Check trade history
sudo docker exec -it freqtrade_freqtrade_1 freqtrade show_trades --config config.live.json
```

## ⚠️ 8. Security Checklist

- [ ] API keys have minimal permissions (no withdrawals)
- [ ] 2FA enabled on Binance account
- [ ] VPS firewall configured
- [ ] SSH key authentication only
- [ ] Environment variables properly secured
- [ ] Regular monitoring enabled

## 🔧 9. Troubleshooting

### Common Issues

1. **Docker build fails**
   ```bash
   docker system prune -a
   make build
   ```

2. **API errors**
   - Check API key permissions
   - Verify IP whitelist on Binance
   - Check API key format

3. **VPS deployment fails**
   - Verify SSH connectivity
   - Check CircleCI environment variables
   - Verify systemd service status

4. **No Telegram notifications**
   - Test bot token with `/getMe` API call
   - Verify chat ID is correct
   - Check bot permissions

### Log Locations

- **Local**: `docker-compose logs -f freqtrade`
- **VPS**: `journalctl -u freqtrade -f`
- **CircleCI**: Check pipeline logs in dashboard

## 📞 Support

- 📚 [Freqtrade Documentation](https://www.freqtrade.io/)
- 💬 [Discord Community](https://discord.gg/p7nuUNVfP7)
- 🐛 GitHub Issues for bot-specific problems

---

**⚠️ Important**: Always test with small amounts first. Trading involves significant risk.