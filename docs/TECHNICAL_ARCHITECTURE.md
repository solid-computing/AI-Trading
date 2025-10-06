# AI Trading Bot - Technical Architecture

**Behind the Scenes: How It Works**

**Version 1.0**  
**Last Updated: 2024**

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Components](#architecture-components)
3. [Infrastructure Layer](#infrastructure-layer)
4. [Application Layer](#application-layer)
5. [Trading Strategy Engine](#trading-strategy-engine)
6. [Data Flow](#data-flow)
7. [Deployment Pipeline](#deployment-pipeline)
8. [Security Architecture](#security-architecture)
9. [Monitoring and Observability](#monitoring-and-observability)
10. [Technical Specifications](#technical-specifications)

---

## System Overview

The AI Trading Bot is a cloud-native automated trading system built on modern DevOps principles. It combines infrastructure-as-code, containerization, continuous deployment, and algorithmic trading to create a robust, scalable trading solution.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│                                                               │
│  ┌──────────────────┐           ┌──────────────────┐        │
│  │  Telegram Bot    │           │  FreqUI Web      │        │
│  │  (Notifications) │           │  (Dashboard)     │        │
│  └──────────────────┘           └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Freqtrade Trading Bot                     │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │ │
│  │  │   Strategy   │  │   Order      │  │   Risk      │ │ │
│  │  │   Engine     │  │   Manager    │  │   Manager   │ │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Integration Layer                         │
│                                                               │
│  ┌──────────────────┐           ┌──────────────────┐        │
│  │   Binance API    │           │  Telegram API    │        │
│  │  (Market Data    │           │  (Notifications) │        │
│  │   & Trading)     │           │                  │        │
│  └──────────────────┘           └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                        │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  OVH VPS (Ubuntu 22.04)                              │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │   Docker   │  │  Systemd   │  │  Network   │     │   │
│  │  │  Runtime   │  │  Service   │  │  Security  │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    DevOps Layer                              │
│                                                               │
│  ┌──────────────────┐           ┌──────────────────┐        │
│  │   Terraform      │           │   CircleCI       │        │
│  │  (Infrastructure)│           │  (CI/CD)         │        │
│  └──────────────────┘           └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture Components

### 1. Trading Engine (Freqtrade)

**Technology**: Python-based algorithmic trading framework

**Core Responsibilities**:
- Market data analysis
- Trade signal generation
- Order execution and management
- Risk management
- Performance tracking

**Key Features**:
- Event-driven architecture
- Plugin-based strategy system
- Exchange abstraction layer
- Built-in backtesting capabilities

### 2. Strategy Module (RsiMaStrategy)

**Implementation**: Custom Python strategy class

**Technical Indicators Used**:
- **RSI (Relative Strength Index)**: Measures overbought/oversold conditions
- **SMA (Simple Moving Average)**: Identifies trend direction
- **MACD (Moving Average Convergence Divergence)**: Momentum indicator
- **Volume**: Confirms price movements
- **Bollinger Bands**: Volatility measurement

**Decision Logic**:
```python
# Entry Signal (simplified)
if (RSI < 30 and 
    Price > SMA and 
    Volume > 1.2 * avg_volume and 
    MACD > Signal_line):
    execute_buy()

# Exit Signal (simplified)
if (RSI > 70 or 
    Price < SMA or 
    MACD < Signal_line):
    execute_sell()
```

### 3. Exchange Integration (Binance)

**Protocol**: REST API + WebSocket

**Data Streams**:
- **Market Data**: Real-time OHLCV (Open, High, Low, Close, Volume)
- **Order Book**: Bid/Ask spreads and depths
- **Trade Execution**: Order placement and status
- **Account Data**: Balance and position updates

**Rate Limiting**:
- Implements request throttling
- Respects exchange rate limits
- Automatic retry with exponential backoff

### 4. Notification System (Telegram)

**Integration**: Bot API

**Message Types**:
- Trade entries and exits
- Error notifications
- Daily summaries
- System status updates
- User commands

### 5. Container Runtime (Docker)

**Base Image**: Python 3.11 slim

**Container Contents**:
- Freqtrade application
- Python dependencies
- Configuration files
- User-defined strategies
- Persistent data volumes

**Benefits**:
- Isolated execution environment
- Reproducible deployments
- Easy version management
- Resource control

---

## Infrastructure Layer

### Cloud Provider: OVH Public Cloud

**Why OVH**:
- Cost-effective European cloud provider
- GDPR compliant
- High-performance network
- Terraform support

### Infrastructure as Code (Terraform)

**Resources Provisioned**:

1. **Compute Instance** (OpenStack Nova)
   ```hcl
   resource "openstack_compute_instance_v2" "freqtrade_vps" {
     name            = "freqtrade-bot"
     flavor_name     = "s1-2"  # 1 vCPU, 2GB RAM
     image_name      = "Ubuntu 22.04"
     key_pair        = "freqtrade-key"
     security_groups = ["freqtrade-sg"]
   }
   ```

2. **Network Configuration**
   - Public IP assignment (floating IP)
   - Private network (optional)
   - DNS configuration

3. **Security Groups** (Firewall Rules)
   ```
   Inbound:
   - Port 22 (SSH) from allowed IP range
   - Port 8080 (FreqUI) from allowed IP range
   
   Outbound:
   - All traffic allowed (for API access)
   ```

4. **SSH Key Pair**
   - RSA 4096-bit key
   - Public key deployed to VPS
   - Private key stored in CircleCI

5. **Data Volumes** (Optional)
   - Persistent storage for trade data
   - Separate from root volume
   - Snapshots for backup

### Server Initialization (Cloud-Init)

**Bootstrap Process**:

```yaml
#cloud-config
packages:
  - docker.io
  - docker-compose
  - git

runcmd:
  # Create freqtrade user
  - useradd -m -s /bin/bash freqtrade
  
  # Add to docker group
  - usermod -aG docker freqtrade
  
  # Setup directories
  - mkdir -p /home/freqtrade/AI-Trading
  
  # Configure firewall
  - ufw allow 22/tcp
  - ufw allow 8080/tcp
  - ufw --force enable
  
  # Enable Docker service
  - systemctl enable docker
  - systemctl start docker
```

### Service Management (Systemd)

**Service Configuration**:

```ini
[Unit]
Description=Freqtrade Trading Bot
After=docker.service
Requires=docker.service

[Service]
Type=simple
User=freqtrade
WorkingDirectory=/home/freqtrade/AI-Trading
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose down
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Benefits**:
- Automatic restart on failure
- Starts on system boot
- Managed logging via journald
- Graceful shutdown handling

---

## Application Layer

### Docker Architecture

**Multi-Stage Build** (Not currently used, but best practice):
```dockerfile
# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY . /app
CMD ["freqtrade", "trade", "--config", "config.json"]
```

**Current Implementation**:
```dockerfile
FROM freqtradeorg/freqtrade:stable

COPY config.dryrun.json /freqtrade/
COPY config.live.template.json /freqtrade/
COPY pairs.json /freqtrade/
COPY user_data/ /freqtrade/user_data/

CMD ["trade", "--config", "config.dryrun.json"]
```

### Configuration Management

**Environment Variables** (`.env`):
```bash
# Sensitive data never committed
BINANCE_API_KEY=xxx
BINANCE_API_SECRET=xxx
TELEGRAM_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
```

**Configuration Files** (JSON):
```json
{
  "exchange": {
    "name": "binance",
    "key": "${BINANCE_API_KEY}",
    "secret": "${BINANCE_API_SECRET}"
  },
  "telegram": {
    "enabled": true,
    "token": "${TELEGRAM_TOKEN}",
    "chat_id": "${TELEGRAM_CHAT_ID}"
  },
  "strategy": "RsiMaStrategy",
  "max_open_trades": 3,
  "stake_amount": 100
}
```

### Strategy Implementation

**File**: `user_data/strategies/RsiMaStrategy.py`

**Class Structure**:
```python
from freqtrade.strategy import IStrategy
from pandas import DataFrame

class RsiMaStrategy(IStrategy):
    # Strategy parameters
    minimal_roi = {
        "0": 0.04,   # 4% at 0 minutes
        "20": 0.02,  # 2% at 20 minutes
        "60": 0.01   # 1% at 60 minutes
    }
    
    stoploss = -0.05  # -5%
    
    timeframe = '5m'  # 5-minute candles
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Calculate technical indicators
        dataframe['rsi'] = ta.RSI(dataframe)
        dataframe['sma'] = ta.SMA(dataframe, timeperiod=50)
        dataframe['macd'], dataframe['signal'], _ = ta.MACD(dataframe)
        dataframe['volume_avg'] = dataframe['volume'].rolling(20).mean()
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Buy signal conditions
        dataframe.loc[
            (dataframe['rsi'] < 30) &
            (dataframe['close'] > dataframe['sma']) &
            (dataframe['volume'] > 1.2 * dataframe['volume_avg']) &
            (dataframe['macd'] > dataframe['signal']),
            'enter_long'] = 1
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Sell signal conditions
        dataframe.loc[
            (dataframe['rsi'] > 70) |
            (dataframe['close'] < dataframe['sma']) |
            (dataframe['macd'] < dataframe['signal']),
            'exit_long'] = 1
        return dataframe
```

---

## Trading Strategy Engine

### How the Trading Algorithm Works

#### 1. Data Collection Phase

**Every 5 minutes**:
1. Fetch OHLCV data from Binance for configured pairs
2. Update in-memory dataframe with new candle
3. Calculate technical indicators
4. Store data for analysis

**Data Structure**:
```
Timestamp | Open | High | Low | Close | Volume | RSI | SMA | MACD | Signal
----------|------|------|-----|-------|--------|-----|-----|------|-------
10:00     | 100  | 102  | 99  | 101   | 1000   | 28  | 98  | 0.5  | 0.3
10:05     | 101  | 103  | 100 | 102   | 1200   | 32  | 99  | 0.6  | 0.4
...
```

#### 2. Signal Generation Phase

**Entry Signal Logic**:
```
AND Logic (All conditions must be true):
├── RSI < 30 (Market oversold)
├── Price > SMA (Upward trend)
├── Volume > 120% of average (High interest)
└── MACD > Signal (Positive momentum)
```

**Exit Signal Logic**:
```
OR Logic (Any condition triggers exit):
├── RSI > 70 (Market overbought)
├── Price < SMA (Trend reversal)
├── MACD < Signal (Momentum loss)
└── ROI target reached
└── Stop loss triggered
```

#### 3. Risk Management

**Position Sizing**:
```python
stake_amount = 100 USDT  # Fixed per trade
max_open_trades = 3       # Maximum concurrent positions
total_exposure = stake_amount * max_open_trades  # 300 USDT max
```

**Stop Loss**:
- Automatically placed at -5% from entry
- Triggers immediately if price drops below threshold
- Prevents catastrophic losses

**ROI (Take Profit)**:
```
Time-based profit targets:
- 0-20 minutes:  4% profit → sell
- 20-60 minutes: 2% profit → sell
- 60+ minutes:   1% profit → sell
```

#### 4. Order Execution

**Order Flow**:
```
1. Generate signal
   ↓
2. Check available balance
   ↓
3. Calculate order size
   ↓
4. Submit limit/market order to Binance
   ↓
5. Wait for order fill confirmation
   ↓
6. Update internal position tracking
   ↓
7. Send Telegram notification
   ↓
8. Monitor position
```

**Order Types**:
- **Entry**: Limit orders (better price)
- **Stop Loss**: Stop-limit orders (automatic exit)
- **Take Profit**: Limit orders (at target price)

---

## Data Flow

### Complete Trading Cycle

```
┌─────────────────────────────────────────────────────────────┐
│  1. Market Data Collection                                   │
│                                                               │
│  Binance API → WebSocket → Freqtrade → DataFrame            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Technical Analysis                                       │
│                                                               │
│  DataFrame → Indicators → RSI, SMA, MACD, Volume            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Signal Generation                                        │
│                                                               │
│  Strategy.populate_entry_trend() → Entry/Exit Signals       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Risk Check                                               │
│                                                               │
│  Check: Balance, Open Trades, Risk Limits                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Order Execution                                          │
│                                                               │
│  Submit Order → Binance API → Order Confirmation            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  6. Position Management                                      │
│                                                               │
│  Track Position → Monitor P&L → Exit Signals                │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  7. Notification                                             │
│                                                               │
│  Telegram API → User Notification                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Pipeline

### CI/CD Architecture (CircleCI)

**Pipeline Stages**:

```yaml
version: 2.1

workflows:
  main:
    jobs:
      - validate      # Lint, test, validate configs
      - build         # Build Docker image
      - terraform     # Provision infrastructure
      - deploy        # Deploy application
```

#### Stage 1: Validation

**Jobs**:
1. **Lint Code**: Check Python syntax and style
2. **Validate Configs**: Verify JSON configuration files
3. **Run Tests**: Execute unit tests (if present)
4. **Backtest Strategy**: Test strategy on historical data

**Commands**:
```bash
python -m py_compile user_data/strategies/RsiMaStrategy.py
python scripts/validate-setup.py
freqtrade backtesting --config config.dryrun.json
```

#### Stage 2: Infrastructure (Terraform)

**Actions**:
1. Initialize Terraform
2. Plan infrastructure changes
3. Apply changes (if approved)

**Terraform Commands**:
```bash
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

**Resources Created**:
- VPS instance
- Network configuration
- Security groups
- SSH keys
- Floating IP

#### Stage 3: Build

**Docker Build Process**:
```bash
docker build -t freqtrade-bot:latest .
docker tag freqtrade-bot:latest freqtrade-bot:${CIRCLE_SHA1}
```

**Image Layers**:
1. Base Freqtrade image
2. Application code
3. Configuration files
4. User strategies
5. Dependencies

#### Stage 4: Deploy

**Deployment Steps**:

```bash
# 1. SSH to VPS
ssh -i ~/.ssh/id_rsa freqtrade@${OVH_HOST}

# 2. Pull latest code
cd ~/AI-Trading
git pull origin main

# 3. Update environment
cat > .env <<EOF
BINANCE_API_KEY=${BINANCE_API_KEY}
BINANCE_API_SECRET=${BINANCE_API_SECRET}
TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
EOF

# 4. Restart service
sudo systemctl restart freqtrade

# 5. Verify deployment
sudo systemctl status freqtrade
```

**Health Checks**:
- Service status verification
- Log analysis for errors
- API connectivity test
- Telegram notification test

### Rollback Strategy

**Automated Rollback Triggers**:
1. Service fails to start
2. Health check failures
3. Critical errors in logs

**Rollback Process**:
```bash
# 1. Stop failed deployment
sudo systemctl stop freqtrade

# 2. Revert to previous version
git checkout <previous-commit>

# 3. Restart service
sudo systemctl start freqtrade

# 4. Verify
sudo systemctl status freqtrade
```

---

## Security Architecture

### Defense in Depth

**Layer 1: Network Security**

- **Firewall (UFW)**:
  ```bash
  ufw allow from <allowed-ip> to any port 22
  ufw allow from <allowed-ip> to any port 8080
  ufw deny from any to any
  ```

- **IP Whitelisting** on Binance API
- **DDoS Protection** from OVH

**Layer 2: Authentication**

- **SSH Key-Based Authentication** (no passwords)
- **API Key Management**:
  - Stored in environment variables
  - Never committed to Git
  - Rotated regularly

**Layer 3: Application Security**

- **Minimal API Permissions**:
  - Spot trading only
  - No withdrawal permissions
  - No futures access

- **Rate Limiting**: Respects exchange limits

**Layer 4: Data Security**

- **Encryption in Transit**: TLS/SSL for all API calls
- **Secrets Management**: CircleCI Contexts
- **No Sensitive Logging**: API keys never logged

### Secrets Management

**CircleCI Context**:
```
Context: freqtrade-secrets
├── BINANCE_API_KEY
├── BINANCE_API_SECRET
├── TELEGRAM_TOKEN
├── TELEGRAM_CHAT_ID
├── OVH_APPLICATION_KEY
├── OVH_APPLICATION_SECRET
└── OVH_CONSUMER_KEY
```

**Environment Variables** (Runtime):
- Injected at container startup
- Not visible in process list
- Isolated per container

---

## Monitoring and Observability

### Logging Architecture

**Log Levels**:
```
DEBUG:   Detailed diagnostic information
INFO:    General informational messages
WARNING: Warning messages
ERROR:   Error messages
CRITICAL: Critical issues
```

**Log Destinations**:

1. **Container Logs** (Docker):
   ```bash
   docker-compose logs -f freqtrade
   ```

2. **System Logs** (Journald):
   ```bash
   journalctl -u freqtrade -f
   ```

3. **Application Logs** (Freqtrade):
   ```
   /home/freqtrade/AI-Trading/user_data/logs/
   ```

### Metrics and Monitoring

**Key Metrics**:

1. **Trading Metrics**:
   - Win rate
   - Profit/Loss
   - Number of trades
   - Average trade duration

2. **System Metrics**:
   - CPU usage
   - Memory usage
   - Disk I/O
   - Network traffic

3. **Application Metrics**:
   - API response times
   - Order execution latency
   - Error rates
   - Uptime

**Monitoring Tools**:
- Telegram notifications (real-time)
- System logs (journalctl)
- FreqUI dashboard (optional)

### Alerting

**Alert Channels**:
1. **Telegram**: Immediate notifications
2. **Logs**: Historical record
3. **Email** (can be configured)

**Alert Types**:
- Trade execution
- Errors and failures
- System issues
- Balance changes
- Daily summaries

---

## Technical Specifications

### Software Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Trading Framework | Freqtrade | Latest stable |
| Language | Python | 3.11+ |
| Container Runtime | Docker | 20.10+ |
| Container Orchestration | Docker Compose | 2.0+ |
| Infrastructure as Code | Terraform | 1.0+ |
| CI/CD | CircleCI | 2.1 |
| Operating System | Ubuntu | 22.04 LTS |
| Service Manager | Systemd | 249+ |

### Infrastructure Requirements

**Minimum VPS Specifications**:
- **CPU**: 1 vCPU
- **RAM**: 2 GB
- **Storage**: 20 GB SSD
- **Network**: 100 Mbps
- **OS**: Ubuntu 22.04 LTS

**Recommended for Production**:
- **CPU**: 2 vCPU
- **RAM**: 4 GB
- **Storage**: 40 GB SSD
- **Backup**: Daily snapshots

### Network Requirements

**Outbound Connections**:
- Binance API: `api.binance.com` (HTTPS/443)
- Telegram API: `api.telegram.org` (HTTPS/443)
- GitHub: `github.com` (HTTPS/443, SSH/22)

**Inbound Connections**:
- SSH: Port 22 (restricted to specific IPs)
- FreqUI: Port 8080 (optional, restricted)

### Performance Characteristics

**Latency**:
- Market data update: ~1-5 seconds
- Order execution: ~100-500ms
- Telegram notification: ~1-3 seconds

**Throughput**:
- Max trades per hour: ~12 (5-minute timeframe)
- API calls per minute: ~20-30
- Data processed per day: ~288 candles per pair

**Resource Usage** (typical):
- CPU: 10-30% average
- RAM: 500 MB - 1 GB
- Disk I/O: Minimal (mostly logs)
- Network: <10 MB/day

---

## Conclusion

The AI Trading Bot represents a sophisticated integration of modern cloud infrastructure, DevOps practices, and algorithmic trading. Its architecture is designed for:

- **Reliability**: Automatic restarts, health checks, and monitoring
- **Security**: Multiple layers of protection for funds and data
- **Scalability**: Can handle multiple trading pairs and strategies
- **Maintainability**: Infrastructure as code and automated deployments
- **Observability**: Comprehensive logging and notifications

This technical foundation enables users to run an automated trading system with minimal manual intervention while maintaining security and reliability.

---

*Document Version: 1.0*  
*For the latest updates, check the GitHub repository.*
