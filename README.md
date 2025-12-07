# 🛡️ RiskLens AI - Blockchain Compliance & Risk Scoring Agent

**Team X07** | **Leader: Vinay** | **Cardano Hackathon**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Masumi](https://img.shields.io/badge/Masumi-Network-purple.svg)](https://masumi.ai)

---

## 🎯 What is RiskLens AI?

RiskLens AI is an **autonomous AI agent** that analyzes blockchain wallet activity to detect risks, suspicious behavior, and compliance issues. It provides instant risk scores and detailed compliance reports for any Cardano wallet address.

### 🌟 Key Features

- ✅ **AI-Powered Analysis** - Multi-agent system using GPT-4
- ✅ **Real Blockchain Data** - Blockfrost API integration for Cardano
- ✅ **Risk Scoring** - 0-100 risk scores with clear categories
- ✅ **Suspicious Pattern Detection** - Identifies scams, mixers, and anomalies
- ✅ **On-Chain Reports** - Tamper-proof results on Cardano blockchain
- ✅ **Pay-Per-Use** - Decentralized payment via Masumi Network
- ✅ **Fast & Accurate** - Results in ~30 seconds
- ✅ **MIP-003 Compliant** - Standard Masumi agent protocol
- ✅ **Easy Integration** - Simple REST API

---

## 🚀 Quick Start

Get started in **5 minutes**! See our [Quick Start Guide](docs/QUICK_START.md).

```bash
# Clone and setup
git clone <repository-url>
cd riskai

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create .env file with:
# - OPENAI_API_KEY
# - BLOCKFROST_PROJECT_ID
# - AGENT_IDENTIFIER
# - PAYMENT_API_KEY
# - SELLER_VKEY
# - MONGO_URL
# - NETWORK=preprod

# Run locally
python main.py api
```

Visit `http://localhost:8000/docs` for interactive API documentation.

---

## 📚 Documentation

### 🎓 Getting Started
- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- **[How It Works](docs/HOW_IT_WORKS.md)** - Simple explanation with examples

### 🏗️ Architecture & Technical
- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design and components
- **[Workflow Documentation](docs/WORKFLOW_DOCUMENTATION.md)** - Complete workflow breakdown
- **[API Reference](docs/API_REFERENCE.md)** - MIP-003 compliant API documentation

### 🚢 Deployment
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Railway deployment steps

📖 **[View All Documentation](docs/README.md)**

---

## 🎯 Use Cases

### For Crypto Exchanges
- KYC/AML compliance checks
- User wallet screening before deposits
- Risk-based account limits
- Automated regulatory reporting

### For DeFi Protocols
- Liquidity provider screening
- Smart contract interaction safety
- Governance participation validation
- Protocol security enhancement

### For Individual Users
- Check wallet reputation before transactions
- Verify counterparty trustworthiness
- Personal compliance monitoring
- Investment due diligence

### For Regulators
- Automated compliance monitoring
- Suspicious activity detection
- Audit trail verification
- Cross-chain analysis

---

## 📊 Risk Scoring System

| Score Range | Category | Color | Description |
|-------------|----------|-------|-------------|
| 0-20 | Low Risk | 🟢 Green | Safe, normal activity |
| 21-50 | Medium Risk | 🟡 Yellow | Some concerns, monitor |
| 51-75 | High Risk | 🟠 Orange | Significant red flags |
| 76-100 | Critical Risk | 🔴 Red | Severe issues, avoid |

---

## 🔍 How It Works

```
1. Submit Wallet Address
   ↓
2. Pay with Cardano (via Masumi)
   ↓
3. AI Analyzes Transactions
   ├─ Fetch real blockchain data (Blockfrost)
   ├─ Detect patterns with AI agents
   └─ Calculate risk score
   ↓
4. Generate Report
   ├─ Risk assessment
   ├─ Suspicious activities
   └─ Recommendations
   ↓
5. Store On-Chain
   ↓
6. Receive Results (formatted string)
```

**Time:** ~30 seconds | **Cost:** 10 ADA per analysis

See [How It Works](docs/HOW_IT_WORKS.md) for detailed explanation.

---

## 🛠️ Technology Stack

- **AI Framework:** CrewAI with OpenAI GPT-4
- **Backend:** FastAPI (Python 3.12+)
- **Payment:** Masumi Network (MIP-003)
- **Blockchain:** Cardano (Preprod/Mainnet)
- **Data Source:** Blockfrost API
- **Database:** MongoDB (Motor async driver)
- **Deployment:** Railway, Kubernetes with Helm

---

## 📡 API Example

### Start Analysis

```bash
curl -X POST https://your-app.up.railway.app/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "user_001",
    "input_data": {
      "wallet_address": "addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgs68faae"
    }
  }'
```

### Check Status

```bash
curl "https://your-app.up.railway.app/status?job_id=<job_id>"
```

![Image1](images/image2.png)
![Image2](images/image.png)


### Response

```json
{
  "job_id": "abc-123",
  "status": "completed",
  "payment_status": "result_submitted",
  "result": "🔍 BLOCKCHAIN WALLET RISK ANALYSIS REPORT\n\n📍 Wallet Address: addr_test1...\n📅 Analysis Date: 2025-12-07T10:30:00Z\n\n📊 RISK ASSESSMENT\n   Risk Score: 25/100\n   Risk Category: Low Risk\n   Trust Score: 75/100\n   Compliance Status: Compliant\n..."
}
```

See [API Reference](docs/API_REFERENCE.md) for complete documentation.

---

## 🚀 Railway Deployment

```bash
# 1. Push to GitHub
git push origin main

# 2. Create Railway project
# - Connect GitHub repository
# - Add MongoDB service
# - Configure environment variables

# 3. Deploy automatically
# Railway will build and deploy your app

# 4. Get your public URL
# https://your-app.up.railway.app
```

See [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) for detailed steps.

---

## 🔐 Security & Privacy

- **No Private Keys Required** - Only analyzes public blockchain data
- **On-Chain Verification** - All reports are verifiable on Cardano
- **Decentralized Processing** - Runs on Masumi Agent Network
- **Transparent Scoring** - Clear explanation of risk factors
- **Tamper-Proof Reports** - Blockchain-stored hashes

---

## 📈 Roadmap

- [x] Core risk analysis engine
- [x] Masumi Network integration (MIP-003)
- [x] Real blockchain data (Blockfrost)
- [x] MongoDB distributed storage
- [x] Railway deployment
- [x] Kubernetes Helm charts
- [ ] Multi-blockchain support (Ethereum, Polygon, BSC)
- [ ] Real-time transaction monitoring
- [ ] Machine learning model training
- [ ] Advanced pattern recognition
- [ ] Dashboard UI
- [ ] Mobile app integration

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team X07

- **Team Leader:** Vinay
- **Project:** RiskLens AI
- **Competition:** Cardano Hackathon 2025

---

## 📞 Support

Need help?

- 📖 [Documentation](docs/README.md)
- 🚀 [Quick Start](docs/QUICK_START.md)
- 🚢 [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- 📡 [API Reference](docs/API_REFERENCE.md)

---

## 🙏 Acknowledgments

- **Masumi Network** - Decentralized agent platform
- **CrewAI** - Multi-agent AI framework
- **OpenAI** - GPT-4 AI capabilities
- **Cardano** - Blockchain infrastructure
- **Blockfrost** - Blockchain API
- **Railway** - Deployment platform

---

## 📊 Project Stats

- **API Endpoints:** 6 (MIP-003 compliant)
- **AI Agents:** 3 (Transaction Analyzer, Risk Scorer, Compliance Reporter)
- **Supported Blockchains:** 1 (Cardano)
- **Average Analysis Time:** 30 seconds
- **Deployment:** Railway + Kubernetes

---

## 🎓 Learn More

- [How It Works](docs/HOW_IT_WORKS.md) - Detailed explanation
- [Architecture](docs/ARCHITECTURE.md) - System design
- [Workflow](docs/WORKFLOW_DOCUMENTATION.md) - Complete flow
- [API Docs](docs/API_REFERENCE.md) - Integration guide

---

**Built with ❤️ by Team X07 for the Cardano Hackathon**

*Making blockchain safer, one wallet at a time* 🛡️

---

## ⭐ Star Us!

If you find RiskLens AI useful, please give us a star on GitHub! It helps us grow and improve.


