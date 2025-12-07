# 📚 RiskLens AI Documentation

Welcome to the RiskLens AI documentation! This directory contains comprehensive guides for understanding, deploying, and using the RiskLens AI blockchain compliance and risk scoring agent.

---

## 📖 Documentation Index

### 🚀 Getting Started
- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
- **[How It Works](HOW_IT_WORKS.md)** - Understanding the system workflow

### 🏗️ Architecture & Technical
- **[Architecture Overview](ARCHITECTURE.md)** - System design and components
- **[Project Structure](PROJECT_STRUCTURE.md)** - Modular directory structure
- **[Workflow Documentation](WORKFLOW_DOCUMENTATION.md)** - Complete workflow breakdown
- **[API Reference](API_REFERENCE.md)** - MIP-003 compliant API endpoints

### 🚢 Deployment
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Railway deployment steps

### 🔧 Development
- **[Complete Refactoring](COMPLETE_REFACTORING.md)** - Modular architecture overview

---

## 🎯 Quick Navigation

### For New Users
1. Start with **[How It Works](HOW_IT_WORKS.md)** to understand the system
2. Follow **[Quick Start Guide](QUICK_START.md)** to get running locally
3. Review **[API Reference](API_REFERENCE.md)** for integration

### For Developers
1. Review **[Architecture Overview](ARCHITECTURE.md)** for system design
2. Check **[Project Structure](PROJECT_STRUCTURE.md)** for code organization
3. Study **[Workflow Documentation](WORKFLOW_DOCUMENTATION.md)** for implementation details
4. Check **[API Reference](API_REFERENCE.md)** for endpoint specifications

### For DevOps/Deployment
1. Follow **[Deployment Guide](DEPLOYMENT_GUIDE.md)** for Railway
2. Configure environment variables as specified in the deployment guide
3. Monitor logs and health endpoints

### For Integrators
1. Study **[API Reference](API_REFERENCE.md)** for MIP-003 endpoints
2. Check **[Workflow Documentation](WORKFLOW_DOCUMENTATION.md)** for job lifecycle
3. Review **[How It Works](HOW_IT_WORKS.md)** for payment flow

---

## 🔑 Key Features

-  **MIP-003 Compliant**: `/availability`, `/input_schema`, `/start_job`, `/status` endpoints
-  **Masumi Payment Integration**: Decentralized payment protocol
-  **Real Blockchain Data**: Blockfrost API integration for Cardano
-  **CrewAI Multi-Agent**: Three specialized AI agents for risk analysis
-  **MongoDB Storage**: Distributed job storage with Railway/Kubernetes support
-  **Modular Architecture**: Clean separation of concerns with agents/, services/, core/, api/
-  **Production Ready**: Health checks, auto-scaling, comprehensive logging

---

## 📝 Current Implementation

### Technology Stack
- **Framework**: FastAPI with async/await
- **AI**: CrewAI with OpenAI GPT-4
- **Blockchain**: Blockfrost API (Cardano preprod/mainnet)
- **Payment**: Masumi Network Protocol
- **Database**: MongoDB (Motor async driver)
- **Deployment**: Railway

### Modular Structure
```
riskai/
├── main.py                    # Entry point
├── agents/                    # AI Agents
│   ├── transaction_analyzer/
│   ├── risk_scorer/
│   └── compliance_reporter/
├── services/                  # Business Services
│   ├── blockchain/
│   ├── payment/
│   └── storage/
├── core/                      # Core Framework
│   ├── config.py
│   ├── logging.py
│   └── crew.py
└── api/                       # API Layer
    ├── models.py
    ├── formatters.py
    └── routes/
```

### Endpoints (MIP-003)
- `GET /` - API information
- `GET /health` - Health check with MongoDB ping
- `GET /availability` - Agent availability status
- `GET /input_schema` - Input requirements
- `POST /start_job` - Create job and payment request
- `GET /status?job_id=<id>` - Check job status

---

## 🆘 Troubleshooting

### Common Issues

**1. Mock Data Instead of Real Blockchain Data**
- **Cause**: `BLOCKFROST_PROJECT_ID` not set
- **Solution**: Add Blockfrost API key to environment variables
- **Verify**: Check logs for "Blockfrost API initialized"

**2. Agent Not Showing on Sokosumi**
- **Cause**: Incorrect callback URL or agent not registered
- **Solution**: Verify callback URL matches deployment URL
- **Check**: Test `/availability` endpoint returns correct `agentIdentifier`

**3. MongoDB Connection Issues**
- **Cause**: Missing or incorrect MongoDB environment variables
- **Solution**: Set `MONGO_URL` or individual `MONGO_HOST`, `MONGO_PORT`, etc.
- **Verify**: Check logs for "Connected to MongoDB successfully"

**4. Environment Variables Not Loading**
- **Cause**: `.env` file not present or loaded after imports
- **Solution**: Ensure `.env` exists and `load_dotenv()` is called before imports
- **Verify**: Check that `AGENT_IDENTIFIER` and other vars are set

**5. Import Errors**
- **Cause**: Old file references or missing modules
- **Solution**: Check [Project Structure](PROJECT_STRUCTURE.md) for correct import paths
- **Verify**: All imports use new modular paths (e.g., `from core.config import settings`)

---

## 📞 Need Help?

- 📖 Check the specific guide for your use case above
- 🐛 Review error messages in logs
- 💬 Verify environment variables are set correctly
- 📧 Ensure Blockfrost and Masumi API keys are valid
- 🏗️ Check [Project Structure](PROJECT_STRUCTURE.md) for code organization

---

## 📅 Documentation Info

**Last Updated:** December 7, 2025  
**Version:** 1.0.0  
**Status:** Production Ready  
**Architecture:** Modular (Refactored December 2025)

---

## 🔄 Recent Updates

### December 7, 2025 - Modular Architecture Refactoring
-  Separated agents into individual folders
-  Extracted payment logic to `services/payment/`
-  Extracted API routes to `api/routes/`
-  Organized services into blockchain, payment, and storage modules
-  Centralized core framework (config, logging, crew)
-  Reduced main.py from 447 to 96 lines (-76%)
-  Improved error handling and logging
-  Fixed environment variable loading order

See [Complete Refactoring](COMPLETE_REFACTORING.md) for details.

---

**Built for Cardano Blockchain Compliance & Risk Assessment**
