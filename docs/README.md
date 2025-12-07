# 📚 RiskLens AI Documentation

Welcome to the RiskLens AI documentation! This directory contains comprehensive guides for understanding, deploying, and using the RiskLens AI blockchain compliance and risk scoring agent.

---

## 📖 Documentation Index

### 🚀 Getting Started
- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
- **[How It Works](HOW_IT_WORKS.md)** - Understanding the system workflow

### 🏗️ Architecture & Technical
- **[Architecture Overview](ARCHITECTURE.md)** - System design and components
- **[Workflow Documentation](WORKFLOW_DOCUMENTATION.md)** - Complete workflow breakdown
- **[API Reference](API_REFERENCE.md)** - MIP-003 compliant API endpoints

### 🚢 Deployment
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Railway deployment steps

---

## 🎯 Quick Navigation

### For New Users
1. Start with **[How It Works](HOW_IT_WORKS.md)** to understand the system
2. Follow **[Quick Start Guide](QUICK_START.md)** to get running locally
3. Review **[API Reference](API_REFERENCE.md)** for integration

### For Developers
1. Review **[Architecture Overview](ARCHITECTURE.md)** for system design
2. Study **[Workflow Documentation](WORKFLOW_DOCUMENTATION.md)** for implementation details
3. Check **[API Reference](API_REFERENCE.md)** for endpoint specifications

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

- ✅ **MIP-003 Compliant**: `/availability`, `/input_schema`, `/start_job`, `/status` endpoints
- ✅ **Masumi Payment Integration**: Decentralized payment protocol
- ✅ **Real Blockchain Data**: Blockfrost API integration for Cardano
- ✅ **CrewAI Multi-Agent**: Three specialized AI agents for risk analysis
- ✅ **MongoDB Storage**: Distributed job storage with Railway/Kubernetes support
- ✅ **Production Ready**: Health checks, auto-scaling, comprehensive logging

---

## 📝 Current Implementation

### Technology Stack
- **Framework**: FastAPI with async/await
- **AI**: CrewAI with OpenAI GPT-4
- **Blockchain**: Blockfrost API (Cardano preprod/mainnet)
- **Payment**: Masumi Network Protocol
- **Database**: MongoDB (Motor async driver)
- **Deployment**: Railway

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
- **Solution**: Add Blockfrost API key to Railway environment variables
- **Verify**: Check logs for "BLOCKFROST API SUCCESSFULLY INITIALIZED"

**2. Agent Not Showing on Sokosumi**
- **Cause**: Incorrect callback URL or agent not registered
- **Solution**: Verify callback URL matches Railway deployment URL
- **Check**: Test `/availability` endpoint returns correct `agentIdentifier`

**3. MongoDB Connection Issues**
- **Cause**: Missing or incorrect MongoDB environment variables
- **Solution**: Set `MONGO_URL` or individual `MONGO_HOST`, `MONGO_PORT`, etc.
- **Verify**: Check logs for "Connected to MongoDB successfully"

**4. Logs Not Showing in Railway**
- **Cause**: Logs only written to file, not console
- **Solution**: Already fixed - logs now output to both file and stdout
- **Verify**: Make a test request and check Railway logs

---

## 📞 Need Help?

- 📖 Check the specific guide for your use case above
- 🐛 Review error messages in Railway logs
- 💬 Verify environment variables are set correctly
- 📧 Ensure Blockfrost and Masumi API keys are valid

---

## 📅 Documentation Info

**Last Updated:** December 7, 2025  
**Version:** 1.0.0  
**Status:** Production Ready

---

**Built for Cardano Blockchain Compliance & Risk Assessment**
