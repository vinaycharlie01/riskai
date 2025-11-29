# 🚀 RiskLens AI - Quick Start Guide

Get RiskLens AI up and running in **5 minutes**!

---

## ⚡ Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.12 or higher
- ✅ OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- ✅ Masumi Payment API Key ([Register here](https://masumi.ai))
- ✅ Git installed

---

## 📦 Step 1: Clone & Setup Virtual Environment (2 minutes)

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

**Note:** Always activate the virtual environment before running the application:
```bash
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

---

## 🔑 Step 2: Configure Environment (1 minute)

Create a `.env` file in the project root:

```bash
# Copy the example
cp .env.example .env

# Edit with your keys
nano .env
```

Add your credentials:

```env
# Required
OPENAI_API_KEY=sk-your-openai-key-here
PAYMENT_API_KEY=your-masumi-payment-key
AGENT_IDENTIFIER=your-agent-identifier
SELLER_VKEY=your-seller-verification-key

# Optional (defaults provided)
PAYMENT_SERVICE_URL=https://payment-service.masumi.ai
NETWORK=Preprod
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
BLOCKFROST_PROJECT_ID=your-blockfrost-key
```

---

## 🎯 Step 3: Test Locally (1 minute)

### Option A: Standalone Mode (No API)

```bash
python main.py
```

This will analyze a sample wallet and display the results.

### Option B: API Mode

```bash
python main.py api
```

The API will start at `http://localhost:8000`

---

## 🧪 Step 4: Try It Out (1 minute)

### Test the API

```bash
# Check if server is running
curl http://localhost:8000/health

# Check availability
curl http://localhost:8000/availability

# Get input schema
curl http://localhost:8000/input_schema
```

### Submit a Risk Analysis

```bash
curl -X POST http://localhost:8000/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "test_001",
    "input_data": {
      "wallet_address": "addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj83ws8lhrn648jjxtwq2ytjqp"
    }
  }'
```

### Check Status

```bash
# Use the job_id from the previous response
curl http://localhost:8000/status?job_id=<your-job-id>
```

---

## 🎉 Success!

You should see:

```json
{
  "job_id": "abc-123-def",
  "status": "completed",
  "payment_status": "completed",
  "result": {
    "wallet_address": "addr_test1...",
    "risk_score": 25,
    "risk_category": "Low Risk",
    ...
  }
}
```

---

## 📊 View API Documentation

Open your browser and visit:

```
http://localhost:8000/docs
```

This shows the interactive Swagger UI with all endpoints.

---

## 🐳 Quick Start with Docker

Prefer Docker? Here's the fastest way:

```bash
# Build the image
docker build -t risklens-ai:latest .

# Run the container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="your-key" \
  -e PAYMENT_API_KEY="your-key" \
  -e AGENT_IDENTIFIER="your-id" \
  -e SELLER_VKEY="your-vkey" \
  risklens-ai:latest
```

---

## 🎯 What's Next?

Now that you're up and running:

1. 📖 Read [How It Works](HOW_IT_WORKS.md) to understand the system
2. 🔧 Check [Setup Guide](SETUP_GUIDE.md) for detailed configuration
3. 🚀 Follow [Deployment Guide](DEPLOYMENT_GUIDE.md) for production
4. 💻 Review [API Reference](API_REFERENCE.md) for integration
5. 📊 See [Usage Examples](USAGE_EXAMPLES.md) for real-world cases

---

## ❓ Common Issues

### Issue: "Module not found"
**Solution:** Make sure you activated the virtual environment and installed dependencies:
```bash
source .venv/bin/activate  # Activate venv first
pip install -r requirements.txt
```

### Issue: "OPENAI_API_KEY not set"
**Solution:** Check your `.env` file exists and has the correct key.

### Issue: "Port 8000 already in use"
**Solution:** Change the port:
```bash
export API_PORT=8080
python main.py api
```

### Issue: "Payment failed"
**Solution:** Verify your Masumi credentials are correct.

---

## 🆘 Need Help?

- 📖 Check the [FAQ](FAQ.md)
- 🐛 [Report an issue](https://github.com/your-repo/issues)
- 💬 Join our community chat
- 📧 Contact: support@risklens.ai

---

## 🎓 Learning Resources

- [How It Works](HOW_IT_WORKS.md) - Understand the workflow
- [Architecture](ARCHITECTURE.md) - System design
- [API Examples](API_EXAMPLES.md) - Code samples
- [Video Tutorial](https://youtube.com/...) - Watch & learn

---

**🎉 Congratulations!** You're now ready to use RiskLens AI!

---

**Built with ❤️ by Team X07 for the Masumi Hackathon**

// Made with Bob
