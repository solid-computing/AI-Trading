# Deployment Checklist

Quick checklist for setting up the AI Trading Bot. See [SETUP.md](./SETUP.md) for detailed instructions.

## ✅ Pre-Deployment Checklist

### 🔐 API Keys & Credentials
- [ ] Created Binance API key with Spot Trading enabled
- [ ] Disabled Futures and Withdrawals on Binance API
- [ ] Set up IP restrictions (optional but recommended)
- [ ] Created Telegram bot via @BotFather
- [ ] Obtained Telegram chat ID
- [ ] Saved all credentials securely

### 🖥️ Infrastructure Setup

#### Option A: Terraform (Recommended)
- [ ] OVH Public Cloud account created
- [ ] OVH API keys generated (https://api.ovh.com/createToken/)
- [ ] Terraform installed (>= 1.0)
- [ ] SSH key pair generated
- [ ] `terraform/terraform.tfvars` configured

#### Option B: Manual VPS Setup
- [ ] VPS provisioned (minimum 2GB RAM, 20GB SSD)
- [ ] SSH access configured
- [ ] `deployment/setup-vps.sh` script executed
- [ ] Environment file created at `/home/freqtrade/.env`
- [ ] SSH keys generated for CircleCI
- [ ] Public key added to VPS authorized_keys

### 🔄 CircleCI Configuration
- [ ] CircleCI project connected to repository
- [ ] Context `freqtrade-secrets` created
- [ ] All environment variables added to context:
  - [ ] `BINANCE_API_KEY`
  - [ ] `BINANCE_API_SECRET`
  - [ ] `TELEGRAM_TOKEN`
  - [ ] `TELEGRAM_CHAT_ID`
  
  **For Terraform (Recommended):**
  - [ ] `OVH_APPLICATION_KEY`
  - [ ] `OVH_APPLICATION_SECRET`
  - [ ] `OVH_CONSUMER_KEY`
  - [ ] `OVH_PROJECT_ID`
  - [ ] `OPENSTACK_USERNAME`
  - [ ] `OPENSTACK_PASSWORD`
  - [ ] `SSH_PUBLIC_KEY`
  
  **For Manual VPS (Alternative):**
  - [ ] `OVH_HOST`
  - [ ] `OVH_USER`
  - [ ] `OVH_SSH_KEY` (base64 encoded)
  - [ ] `OVH_SSH_FINGERPRINT`

### 🧪 Local Testing
- [ ] Repository cloned locally
- [ ] Local `.env` file created
- [ ] `make validate` passed
- [ ] `make quick-start` successful
- [ ] Bot runs in dry-run mode
- [ ] Telegram notifications working

## 🚀 Deployment Steps

### Fully Automated with CircleCI (Recommended)
- [ ] Configure CircleCI with all required environment variables above
- [ ] Push changes to main branch
- [ ] Monitor CircleCI pipeline (infrastructure → build → deploy)
- [ ] Verify deployment success in CircleCI and VPS

### Manual Infrastructure + Auto Deployment  
- [ ] Copy `terraform/terraform.tfvars.example` to `terraform/terraform.tfvars`
- [ ] Fill in OVH API credentials in terraform.tfvars
- [ ] Run `make terraform-deploy` to create infrastructure
- [ ] Configure CircleCI with deployment credentials only
- [ ] Push to main branch for automatic application deployment

### Manual VPS + Auto Deployment (Alternative)
- [ ] Set up VPS manually using `deployment/setup-vps.sh`
- [ ] Configure CircleCI with VPS credentials
- [ ] Push to main branch for automatic application deployment

### Fully Manual (Development/Testing)
- [ ] Run `make terraform-deploy` or set up VPS manually
- [ ] Run `make deploy-terraform` or `make deploy`
- [ ] Verify deployment manually

## ✅ Post-Deployment Verification

### Service Status
- [ ] `sudo systemctl status freqtrade` shows active
- [ ] Docker containers running
- [ ] No errors in logs

### Bot Functionality
- [ ] Telegram bot responds to `/status`
- [ ] Trading notifications received
- [ ] Balance commands working
- [ ] Logs show proper market data

### Monitoring Setup
- [ ] Log monitoring configured
- [ ] Telegram alerts working
- [ ] Regular backup strategy in place

## 🔧 Quick Commands Reference

```bash
# Local Development
make validate              # Validate setup
make quick-start          # Start in dry-run mode
make logs                 # View logs
make down                 # Stop bot

# VPS Management
sudo systemctl status freqtrade    # Check service
journalctl -u freqtrade -f         # View logs
sudo systemctl restart freqtrade   # Restart service

# Deployment
make deploy               # Manual deploy
git push origin main      # Trigger auto-deploy
```

## 🆘 Emergency Commands

```bash
# Stop trading immediately
sudo systemctl stop freqtrade

# Emergency trade exit (if needed)
sudo docker exec -it freqtrade_freqtrade_1 freqtrade cancel_open_orders

# Check account balance
sudo docker exec -it freqtrade_freqtrade_1 freqtrade show_balance
```

---

**Remember**: Always test with small amounts first!