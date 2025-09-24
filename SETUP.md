# Setup Guide - AI Trading Bot

This guide outlines what you need to configure manually before using the automated deployment.

## 🎯 Quick Overview

**What You Need to Do Manually (One-time Setup):**
1. Get API keys from Binance and Telegram
2. Set up OVH Cloud account and API keys (for Terraform)
3. Configure CircleCI with your credentials
4. Choose deployment method and run commands

**What's Automated:**
- Infrastructure provisioning (via Terraform)
- VPS setup and configuration
- Application deployment and updates
- Service management and monitoring

---

## 📋 Manual Setup Required

### 🔐 Step 1: Get API Credentials (Required)

#### Binance API Keys
1. **Login to Binance** → [API Management](https://www.binance.com/en/my/settings/api-management)
2. **Create API** with label "Trading Bot"
3. **Set Permissions:**
   - ✅ Enable Spot & Margin Trading
   - ❌ Disable Futures Trading (safety)
   - ❌ Disable Withdrawals (security)
4. **Save these values:**
   ```
   BINANCE_API_KEY=your_actual_api_key_here
   BINANCE_API_SECRET=your_actual_secret_here
   ```

#### Telegram Bot Setup
1. **Message [@BotFather](https://t.me/BotFather)** → Send `/newbot`
2. **Choose bot name** and username
3. **Save the token:**
   ```
   TELEGRAM_TOKEN=your_bot_token_here
   ```
4. **Get your chat ID:**
   - Message your bot, then visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Find your chat ID in the response
   ```
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

### 🏗️ Step 2: Infrastructure Setup (Choose One)

#### Option A: Terraform + CircleCI (Recommended - Fully Automated)

**What you configure once:**
1. **OVH Cloud Account:**
   - Sign up at [OVH Public Cloud](https://www.ovhcloud.com/en/public-cloud/)
   - Create a project
   - Generate API keys at https://api.ovh.com/createToken/

2. **CircleCI Configuration:**
   - Connect your GitHub repo to CircleCI
   - Add these environment variables to CircleCI Context `freqtrade-secrets`:

   | Variable | Value | Where to Get |
   |----------|-------|--------------|
   | `BINANCE_API_KEY` | Your Binance API key | Step 1 above |
   | `BINANCE_API_SECRET` | Your Binance API secret | Step 1 above |
   | `TELEGRAM_TOKEN` | Your Telegram bot token | Step 1 above |
   | `TELEGRAM_CHAT_ID` | Your Telegram chat ID | Step 1 above |
   | `OVH_APPLICATION_KEY` | OVH API application key | https://api.ovh.com/createToken/ |
   | `OVH_APPLICATION_SECRET` | OVH API application secret | https://api.ovh.com/createToken/ |
   | `OVH_CONSUMER_KEY` | OVH API consumer key | https://api.ovh.com/createToken/ |
   | `OVH_PROJECT_ID` | OVH Public Cloud project ID | OVH Control Panel |
   | `OPENSTACK_USERNAME` | Your OVH username | OVH Account |
   | `OPENSTACK_PASSWORD` | Your OVH password | OVH Account |
   | `SSH_PUBLIC_KEY` | Your SSH public key content | Generate with `ssh-keygen` |

**What happens automatically:**
- ✅ Infrastructure provisioning (VPS, networking, security)
- ✅ VPS configuration (Docker, users, firewall)
- ✅ Application deployment
- ✅ Service startup and monitoring

**To deploy:** Just push to main branch!

#### Option B: Manual VPS + CircleCI (Semi-Automated)

**What you do manually:**
1. **Get a VPS** (OVH recommended, min 2GB RAM, 20GB SSD)
2. **Run setup script** on your VPS:
   ```bash
   wget https://github.com/solid-computing/AI-Trading/raw/main/deployment/setup-vps.sh
   chmod +x setup-vps.sh
   sudo ./setup-vps.sh
   ```
3. **Configure environment file** on VPS:
   ```bash
   sudo nano /home/freqtrade/.env
   # Add your API keys from Step 1
   ```
4. **Add to CircleCI Context** `freqtrade-secrets`:
   - All API keys from Step 1
   - `OVH_HOST` = your VPS IP address
   - `OVH_USER` = freqtrade
   - `OVH_SSH_KEY` = base64 encoded private key
   - `OVH_SSH_FINGERPRINT` = SSH key fingerprint

**What happens automatically:**
- ✅ Application deployment
- ✅ Service updates
- ✅ Configuration management

#### Option C: Local Development/Testing

**What you do manually:**
1. **Clone repository**
2. **Create `.env` file** with your API keys from Step 1
3. **Run commands:**
   ```bash
   make validate    # Check setup
   make up         # Start in dry-run mode
   make logs       # Monitor
   ```

**What happens automatically:**
- ✅ Docker container management
- ✅ Configuration validation
- ✅ Local testing environment

---

## 🚀 Deployment Methods

### Fully Automated (Terraform + CircleCI)
```bash
# One-time setup: Configure CircleCI with credentials above
# Then just:
git push origin main
# Everything else is automatic!
```

### Semi-Automated (Manual VPS + CircleCI)  
```bash
# One-time setup: VPS + CircleCI configuration
# Then:
git push origin main
# Application deploys automatically
```

### Manual Control (Local + Make Commands)
```bash
# For infrastructure:
make terraform-deploy    # Create OVH infrastructure

# For application:
make deploy-terraform    # Deploy to Terraform VPS
# OR
make deploy             # Deploy to manual VPS
```

---

## 🔍 What Each Method Provides

| Feature | Terraform+CI | Manual+CI | Local Dev |
|---------|--------------|-----------|-----------|
| Infrastructure Creation | ✅ Automatic | ❌ Manual | ❌ Manual |
| VPS Configuration | ✅ Automatic | ❌ Manual | N/A |
| App Deployment | ✅ Automatic | ✅ Automatic | ❌ Manual |
| Updates | ✅ Git Push | ✅ Git Push | ❌ Manual |
| Cost Management | ✅ Destroy via tag | ❌ Manual | ✅ Local only |
| Production Ready | ✅ Yes | ✅ Yes | ❌ Development |

---

## 💰 Cost Estimates (OVH)

- **Small Bot**: s1-2 instance (~€3-5/month) - 1 vCPU, 2GB RAM
- **Medium Load**: s1-4 instance (~€6-8/month) - 1 vCPU, 4GB RAM  
- **High Frequency**: s1-8 instance (~€12-15/month) - 2 vCPU, 8GB RAM
- **Storage**: €0.04/GB/month for additional volumes

---

## 🆘 Quick Troubleshooting

**CircleCI fails:** Check all environment variables are set in Context `freqtrade-secrets`

**Terraform fails:** Verify OVH API keys have correct permissions for `/cloud/*`

**Deployment fails:** Check SSH keys and VPS connectivity

**Bot not trading:** Verify Binance API keys have correct permissions and IP restrictions

**No notifications:** Test Telegram bot token with `/getMe` API call

---

**Next:** After completing the manual setup above, everything else is automated!
