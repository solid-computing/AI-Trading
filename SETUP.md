# Manual Setup Guide - AI Trading Bot

This guide provides step-by-step instructions for the manual configuration needed before deployment.

## Prerequisites

Before starting the setup, ensure you have:

### Option A: Terraform Infrastructure (Recommended)
- OVH Public Cloud account
- Terraform >= 1.0 installed
- Basic command line knowledge
- SSH key pair

### Option B: Manual VPS Setup
- A VPS (OVH recommended, minimum 2GB RAM, 20GB SSD)  
- SSH access to the VPS
- Basic command line knowledge

### For Both Options
- Binance account with API access
- Telegram bot token
- CircleCI account (for automated deployment)

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

## 🏗️ 2. Infrastructure Setup (Choose One)

### Option A: Terraform Infrastructure (Recommended)

1. **Install Terraform**
   ```bash
   # Ubuntu/Debian
   wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
   sudo apt update && sudo apt install terraform
   
   # macOS
   brew install terraform
   ```

2. **Get OVH API Keys**
   - Go to https://api.ovh.com/createToken/
   - Application name: "AI Trading Bot"
   - Rights: `GET/POST/PUT/DELETE /cloud/*`
   - Save: Application Key, Application Secret, Consumer Key

3. **Configure Terraform Variables**
   ```bash
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   nano terraform.tfvars
   ```
   
   Fill in your values:
   ```hcl
   ovh_application_key    = "your_ovh_application_key"
   ovh_application_secret = "your_ovh_application_secret"
   ovh_consumer_key      = "your_ovh_consumer_key"
   ovh_project_id        = "your_ovh_project_id"
   openstack_username     = "your_ovh_username"
   openstack_password     = "your_ovh_password"
   ```

4. **Generate SSH Key (if needed)**
   ```bash
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -C "ai-trading-bot"
   ```

5. **Deploy Infrastructure**
   ```bash
   # From project root
   make terraform-deploy
   
   # Or manually:
   cd terraform
   ./deploy.sh
   ```

6. **Note the Outputs**
   ```bash
   # Get connection details
   cd terraform && terraform output
   
   # Save these for deployment:
   export OVH_HOST=$(terraform output -raw public_ip)
   export OVH_USER=freqtrade
   ```

### Option B: Manual VPS Setup

## 🖥️ 3. Manual VPS Setup (Alternative to Terraform)

### 3.1 Server Preparation

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

### 3.2 SSH Key Setup

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

## 🔄 4. CircleCI Configuration

### 4.1 Create Context

1. **Go to CircleCI**
   - Navigate to Organization Settings → Contexts
   - Click "Create Context"
   - Name it: `freqtrade-secrets`

### 4.2 Add Environment Variables

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

### 4.3 Get SSH Fingerprint

```bash
# On your local machine
ssh-keygen -lf ~/.ssh/id_rsa_circleci
# Copy the fingerprint (format: SHA256:xxxxx)
```

## 🧪 5. Local Testing

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

## 📋 6. Configuration Files

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

## 🚀 7. Deployment Process

### 7.1 Terraform Deployment (Recommended)

```bash
# Deploy application to Terraform-provisioned infrastructure
make deploy-terraform

# Or manually with environment variables:
export OVH_HOST=$(cd terraform && terraform output -raw public_ip)
export OVH_USER=freqtrade
./deployment/deploy-terraform.sh
```

### 7.2 Manual Deployment

```bash
# Deploy to VPS manually
export OVH_HOST=your_vps_ip
export OVH_USER=root
make deploy
```

### 7.3 Automatic Deployment

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

## 🛠️ 8. Post-Deployment Verification

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

## ⚠️ 9. Security Checklist

- [ ] API keys have minimal permissions (no withdrawals)
- [ ] 2FA enabled on Binance account
- [ ] VPS firewall configured
- [ ] SSH key authentication only
- [ ] Environment variables properly secured
- [ ] Regular monitoring enabled

## 🔧 10. Troubleshooting

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

## 📞 11. Support

- 📚 [Freqtrade Documentation](https://www.freqtrade.io/)
- 💬 [Discord Community](https://discord.gg/p7nuUNVfP7)
- 🐛 GitHub Issues for bot-specific problems

---

**⚠️ Important**: Always test with small amounts first. Trading involves significant risk.