# Freqtrade Trading Bot

Automated cryptocurrency trading bot for Binance with complete CI/CD and VPS deployment.

## Architecture

```mermaid
graph TB
    subgraph "Trading System"
        A[Freqtrade Bot] --> B[Binance API]
        A --> C[Telegram Bot]
        A --> D[RsiMaStrategy]
    end
    
    subgraph "Infrastructure"
        E[CircleCI] --> F[OVH VPS]
        G[Docker] --> A
        H[Systemd] --> G
    end
    
    subgraph "Monitoring"
        C --> I[Telegram Notifications]
        A --> J[Logs & Metrics]
    end
    
    B -.-> K[Market Data]
    D --> L[Technical Indicators]
```

## Features

- **Exchange**: Binance Spot | **Notifications**: Telegram | **Strategy**: RSI+MA+MACD+Volume
- **Local**: Docker Compose | **Production**: systemd service | **CI/CD**: CircleCI pipeline

## Quick Start

```mermaid
graph LR
    A[Local Development] --> B[docker-compose up -d]
    C[VPS Deployment] --> D[./deployment/setup-vps.sh]
    D --> E[Configure secrets]
    E --> F[git push origin main]
    F --> G[CircleCI Auto-Deploy]
```

**📋 [Complete Setup Guide](./SETUP.md)** | **✅ [Deployment Checklist](./DEPLOYMENT_CHECKLIST.md)**

**Local**: `make quick-start` or `docker-compose up -d`  
**VPS**: Run `deployment/setup-vps.sh` → Configure secrets → Push to main branch

## Configuration

```mermaid
graph TD
    A[config.dryrun.json] --> B[Local Testing]
    C[config.live.template.json] --> D[Production]
    E[pairs.json] --> F[Trading Pairs]
    G[CircleCI Context] --> H[Secrets]
    
    subgraph "Secrets"
        H --> I[BINANCE_API_KEY/SECRET]
        H --> J[TELEGRAM_TOKEN/CHAT_ID]
        H --> K[OVH_SSH_KEY/HOST/USER]
    end
```

**Files**: `config.dryrun.json` (testing) | `config.live.template.json` (production) | `pairs.json` (pairs)  
**Secrets**: Set in CircleCI Context `freqtrade-secrets`

## Strategy: RsiMaStrategy

```mermaid
graph TB
    subgraph "Entry Signals"
        A[RSI < 30] --> E[BUY]
        B[Price > SMA] --> E
        C[Volume > 1.2x avg] --> E
        D[MACD > Signal] --> E
    end
    
    subgraph "Exit Signals"
        F[RSI > 70] --> I[SELL]
        G[Price < SMA] --> I
        H[MACD < Signal] --> I
    end
    
    subgraph "Risk Management"
        J[Stop Loss: -5%] --> K[Max Trades: 3]
        L[ROI: 4%→2%→1%] --> K
    end
```

**Indicators**: RSI + SMA + Volume + MACD + Bollinger Bands  
**Risk**: -5% stop loss, ROI table, max 3 trades

## Development

```mermaid
graph LR
    A[make validate] --> B[make build]
    B --> C[make up]
    C --> D[make logs]
    
    E[Code Changes] --> F[make lint]
    F --> G[make test]
    G --> H[git push]
```

**Commands**: `make quick-start` | `make validate` | `make logs` | `make down`

## CI/CD Pipeline

```mermaid
graph LR
    A[Git Push] --> B[CircleCI]
    B --> C[Lint & Test]
    B --> D[Backtest]
    B --> E[Build Docker]
    C --> F[Deploy to VPS]
    D --> F
    E --> F
    F --> G[Systemd Restart]
    
    style F fill:#e1f5fe
    style G fill:#e8f5e8
```

## Monitoring

```mermaid
graph TB
    A[Trading Bot] --> B[Telegram Notifications]
    A --> C[System Logs]
    A --> D[FreqUI Dashboard]
    
    B --> E[Trade Entries/Exits]
    B --> F[Errors & Warnings]
    B --> G[Daily Summaries]
    
    C --> H[journalctl -u freqtrade -f]
    D --> I[http://localhost:8081]
```

**Local**: `make logs` | **VPS**: `journalctl -u freqtrade -f` | **UI**: http://localhost:8081

## Security & Troubleshooting

```mermaid
graph TB
    subgraph "Security"
        A[Environment Variables] --> B[CircleCI Context]
        C[Minimal API Permissions] --> D[Spot Trading Only]
        E[2FA Enabled] --> F[Regular Monitoring]
    end
    
    subgraph "Common Issues"
        G[Docker Build Fails] --> H[docker system prune -a]
        I[API Errors] --> J[Check Keys & Whitelist]
        K[VPS Deploy Fails] --> L[Check SSH & Service]
    end
```

**Security**: Environment variables only | Minimal API permissions | 2FA enabled  
**Cost**: OVH VPS SSD 1 (~€3-€5/month) | 1 vCPU, 2GB RAM, 20GB SSD

## ⚠️ Disclaimer

**Trading cryptocurrencies involves significant risk**. Educational purposes only.  
Always test with dry-run mode and small amounts.

## Support

📚 [Freqtrade Docs](https://www.freqtrade.io/) | 💬 [Discord](https://discord.gg/p7nuUNVfP7) | 🐛 GitHub Issues

## 📋 Setup Documentation

- **[SETUP.md](./SETUP.md)** - Complete manual setup guide with step-by-step instructions
- **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** - Quick checklist for deployment
- **[.env.example](./.env.example)** - Environment variables template
