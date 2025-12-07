# 🚀 RiskLens AI - Quick Start Guide

Get RiskLens AI up and running in **5 minutes**!

---

## ⚡ Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.12 or higher
- ✅ OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- ✅ Blockfrost API Key ([Get free key](https://blockfrost.io))
- ✅ Masumi Agent Registration ([Register here](https://sokosumi.com))
- ✅ MongoDB (Railway, Atlas, or local)
- ✅ Git installed

---

## 📦 Step 1: Clone & Setup (2 minutes)

```bash
# Clone the repository
git clone <repository-url>
cd riskai

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note:** Always activate the virtual environment before running:
```bash
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

---

## 🔑 Step 2: Configure Environment (2 minutes)

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add your credentials:

```env
# OpenAI (Required for AI analysis)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx

# Blockfrost (Required for real blockchain data)
BLOCKFROST_PROJECT_ID=preprodxxxxxxxxxxxxxxxxxxxxx
NETWORK=preprod

# Masumi Integration (Required for payments)
AGENT_IDENTIFIER=your-agent-identifier
PAYMENT_SERVICE_URL=https://api.masumi.network
PAYMENT_API_KEY=your-masumi-api-key
SELLER_VKEY=your-seller-verification-key

# MongoDB (Required for job storage)
# Option 1: MongoDB URL (Railway or Atlas)
MONGO_URL=mongodb://user:pass@host:port/database
MONGO_DB=risklens_ai

# Option 2: Individual MongoDB variables (Kubernetes)
# MONGO_HOST=mongodb
# MONGO_PORT=27017
# MONGO_USER=username
# MONGO_PASSWORD=password
# MONGO_DB=risklens_ai

# API Configuration (Optional)
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 🎯 Step 3: Run Locally (1 minute)

### Option A: Standalone Mode (Test AI Analysis)

```bash
python main.py
```

This will:
- Analyze a sample wallet address
- Display the risk analysis report
- Test the AI agents without API/payments

### Option B: API Mode (Full Masumi Integration)

```bash
python main.py api
```

The API will start at `http://localhost:8000`

You'll see:
```
🚀 Starting FastAPI server with Masumi integration...
======================================================================
API Documentation:        http://0.0.0.0:8000/docs
Availability Check:       http://0.0.0.0:8000/availability
Status Check:             http://0.0.0.0:8000/status
Input Schema:             http://0.0.0.0:8000/input_schema
======================================================================
```

---

## 🧪 Step 4: Test the API

### Check Server Health

```bash
# Health check (includes MongoDB ping)
curl http://localhost:8000/health

# Expected: {"status": "healthy"}
```

### Check Agent Availability (MIP-003)

```bash
curl http://localhost:8000/availability
```

Expected response:
```json
{
  "status": "available",
  "type": "masumi-agent",
  "agentIdentifier": "your-agent-id",
  "message": "Server operational."
}
```

### Get Input Schema (MIP-003)

```bash
curl http://localhost:8000/input_schema
```

Expected response:
```json
{
  "input_data": [
    {
      "id": "wallet_address",
      "type": "string",
      "name": "Wallet Address",
      "data": {
        "description": "The blockchain wallet address to analyze...",
        "placeholder": "Enter wallet address (e.g., 0x742d35...)"
      }
    }
  ]
}
```

### Start a Risk Analysis Job

```bash
curl -X POST http://localhost:8000/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "test_001",
    "input_data": {
      "wallet_address": "addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgs68faae"
    }
  }'
```

Response includes:
```json
{
  "status": "success",
  "job_id": "abc-123-def-456",
  "blockchainIdentifier": "payment-id",
  "submitResultTime": 1234567890,
  ...
}
```

### Check Job Status

```bash
# Use the job_id from previous response
curl "http://localhost:8000/status?job_id=abc-123-def-456"
```

Response:
```json
{
  "job_id": "abc-123-def-456",
  "status": "completed",
  "payment_status": "result_submitted",
  "result": "🔍 BLOCKCHAIN WALLET RISK ANALYSIS REPORT\n\n📍 Wallet Address: addr_test1...\n..."
}
```

---

## 📊 Interactive API Documentation

Open your browser and visit:

```
http://localhost:8000/docs
```

This shows the **Swagger UI** with:
- ✅ All MIP-003 endpoints
- ✅ Try it out functionality
- ✅ Request/response examples
- ✅ Schema definitions

---

## 🎉 Verify Everything Works

### 1. Check Blockfrost Integration

Look for these logs when starting the API:

**✅ Good (Real Data):**
```
✅ BLOCKFROST_PROJECT_ID found: preprod1...xyz
✅ BLOCKFROST API SUCCESSFULLY INITIALIZED!
✅ Will fetch REAL blockchain data from Cardano preprod
```

**❌ Bad (Mock Data):**
```
❌ BLOCKFROST_PROJECT_ID NOT SET!
⚠️  Will use MOCK DATA for all requests
```

### 2. Check MongoDB Connection

**✅ Good:**
```
✅ Connected to MongoDB successfully
📂 Database: risklens_ai
```

**❌ Bad:**
```
❌ Failed to connect to MongoDB: ...
```

### 3. Test a Real Wallet

Make a request with a real Cardano preprod address and verify:
- Different addresses return different results
- Transaction counts vary
- ADA amounts are realistic
- Risk scores are calculated based on actual data

---

## 🐳 Quick Start with Docker

```bash
# Build the image
docker build -t risklens-ai:latest .

# Run with environment variables
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="sk-proj-xxx" \
  -e BLOCKFROST_PROJECT_ID="preprodxxx" \
  -e AGENT_IDENTIFIER="your-id" \
  -e PAYMENT_API_KEY="your-key" \
  -e SELLER_VKEY="your-vkey" \
  -e MONGO_URL="mongodb://..." \
  -e NETWORK="preprod" \
  risklens-ai:latest
```

---

## 🚀 Deploy to Railway

For production deployment:

1. Push code to GitHub
2. Create Railway project
3. Add MongoDB service
4. Configure environment variables
5. Deploy automatically

See [Deployment Guide](DEPLOYMENT_GUIDE.md) for detailed steps.

---

## 🎯 What's Next?

Now that you're up and running:

1. 📖 Read [How It Works](HOW_IT_WORKS.md) to understand the system
2. 🏗️ Check [Architecture](ARCHITECTURE.md) for system design
3. 🚀 Follow [Deployment Guide](DEPLOYMENT_GUIDE.md) for Railway
4. 💻 Review [API Reference](API_REFERENCE.md) for MIP-003 endpoints
5. 🔧 See [Workflow Documentation](WORKFLOW_DOCUMENTATION.md) for details

---

## ❓ Common Issues

### Issue: "BLOCKFROST_PROJECT_ID NOT SET"
**Symptom:** Same results for different wallet addresses  
**Solution:** 
1. Get free API key from https://blockfrost.io/
2. Add to `.env`: `BLOCKFROST_PROJECT_ID=preprodxxx`
3. Restart the application

### Issue: "Failed to connect to MongoDB"
**Solution:** 
1. Check `MONGO_URL` is correct
2. Verify MongoDB is running
3. Test connection string format: `mongodb://user:pass@host:port/database`

### Issue: "AGENT_IDENTIFIER not set"
**Solution:** 
1. Register agent at https://sokosumi.com/
2. Add to `.env`: `AGENT_IDENTIFIER=your-agent-id`
3. Restart the application

### Issue: "Module not found"
**Solution:** 
```bash
source .venv/bin/activate  # Activate venv first
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution:** 
```bash
export API_PORT=8080
python main.py api
```

---

## 🆘 Need Help?

- 📖 Check [Deployment Guide](DEPLOYMENT_GUIDE.md) for troubleshooting
- 📚 Review [API Reference](API_REFERENCE.md) for endpoint details
- 🔧 See [Workflow Documentation](WORKFLOW_DOCUMENTATION.md) for flow
- 💬 Check Masumi docs: https://docs.masumi.network/

---

## 🎓 Learning Resources

- [How It Works](HOW_IT_WORKS.md) - System workflow
- [Architecture](ARCHITECTURE.md) - Technical design
- [Masumi Integration](MASUMI_INTEGRATION.md) - Payment protocol
- [Code Review](CODE_REVIEW.md) - Code quality

---

**🎉 Congratulations!** You're now ready to use RiskLens AI!

---

**Built for Cardano Blockchain Compliance & Risk Assessment**

// Made with Bob
