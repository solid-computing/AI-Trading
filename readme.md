# AI-Enhanced Freqtrade Trading Bot

Automated cryptocurrency trading bot for Binance with **Advanced AI Reasoning** capabilities, complete CI/CD and VPS deployment.

## 🤖 AI-Enhanced Features

This project integrates cutting-edge AI reasoning into FreqTrade to leverage modern AI advancements:

- **🧠 Market Regime Detection**: AI identifies bull, bear, sideways, volatile, and crash market conditions
- **📊 Multi-Modal Sentiment Analysis**: Combines social media, news, and market metrics
- **⚖️ Dynamic Risk Management**: AI-optimized position sizing and stop-loss levels
- **🎯 Real-time Decision Making**: AI analyzes market conditions and adapts strategy in real-time
- **🚨 Emergency Detection**: AI monitors for market crashes and anomalies
- **📈 Adaptive Parameters**: Strategy parameters automatically adjust to market conditions

## Architecture

```mermaid
graph TB
    subgraph "AI-Enhanced Trading System"
        A[Freqtrade Bot] --> B[Binance API]
        A --> C[Telegram Bot]
        A --> D[AI-Enhanced Strategy]
        D --> AI[AI Decision Engine]
    end
    
    subgraph "AI Intelligence Layer"
        AI --> MA[Market Analyzer]
        AI --> SE[Sentiment Engine]
        AI --> RM[Risk Manager]
        MA --> |Regime Detection| AI
        SE --> |Sentiment Analysis| AI
        RM --> |Position Sizing| AI
    end
    
    subgraph "Infrastructure"
        E[CircleCI] --> F[OVH VPS]
        G[Docker] --> A
        H[Systemd] --> G
        T[Terraform] --> F
    end
    
    subgraph "Monitoring"
        C --> I[Telegram Notifications]
        A --> J[Logs & Metrics]
        AI --> K[AI Decision Logs]
    end
    
    B -.-> L[Market Data]
    MA --> M[Technical Indicators]
    SE --> N[Market Psychology]
```

## Features

### 🤖 AI-Powered Trading
- **AI-Enhanced Strategy**: Traditional RSI+MA enhanced with AI reasoning
- **Market Regime Adaptation**: Different behavior in bull/bear/volatile markets  
- **Sentiment Integration**: Social media, news, and market psychology analysis
- **Dynamic Risk Management**: AI-optimized position sizing and stop losses
- **Emergency Detection**: Automatic exits during market crashes or anomalies
- **Real-time Learning**: AI adapts parameters based on market conditions

### 🏗️ Infrastructure & Deployment
- **Exchange**: Binance Spot | **Notifications**: Telegram | **Strategy**: AI-Enhanced RSI+MA
- **Local**: Docker Compose | **Production**: systemd service | **CI/CD**: CircleCI pipeline
- **Infrastructure**: Terraform for OVH Cloud | **Deployment**: Automated with make commands
- **AI Components**: Market Analyzer, Sentiment Engine, Risk Manager, Decision Engine

## Quick Start

```mermaid
graph LR
    A[Local Development] --> B[docker-compose up -d]
    
    C[Fully Automated] --> D[Configure CircleCI]
    D --> E[git push origin main]
    E --> F[Auto: Infrastructure + Deploy]
    
    G[Manual Control] --> H[make terraform-deploy]
    H --> I[make deploy-terraform]
    
    J[Traditional VPS] --> K[./deployment/setup-vps.sh]
    K --> L[Configure CircleCI]
    L --> M[git push → Auto Deploy]
```

**📋 [Complete Setup Guide](./SETUP.md)** | **✅ [Deployment Checklist](./DEPLOYMENT_CHECKLIST.md)** | **🏗️ [Terraform Guide](./terraform/README.md)**

**Fully Automated**: Configure CircleCI → `git push origin main` → Everything automatic!  
**Manual Control**: `make terraform-deploy` → `make deploy-terraform`  
**Local Dev**: `make quick-start` or `docker-compose up -d`

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
    B --> D[Terraform Validate]
    B --> E[Backtest]
    B --> F[Build Docker]
    
    C --> G[Terraform Plan]
    D --> G
    E --> G
    F --> G
    
    G --> H[Terraform Apply]
    H --> I[Deploy Application]
    I --> J[Service Health Check]
    
    style G fill:#fff3e0
    style H fill:#e1f5fe
    style I fill:#e8f5e8
    style J fill:#f3e5f5
```

**Pipeline Features:**
- **Infrastructure as Code**: Terraform validates and provisions OVH infrastructure
- **Automated Testing**: Linting, backtesting, and Docker builds
- **Zero-Touch Deployment**: Complete infrastructure + application deployment
- **Health Monitoring**: Automatic service verification and rollback capability

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
