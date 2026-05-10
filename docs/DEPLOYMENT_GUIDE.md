# 🚀 RiskLens AI Deployment Guide

Complete guide for deploying RiskLens AI to Railway with Masumi integration.

---

## 📋 Prerequisites

Before deploying, ensure you have:

1. **Railway Account**: Sign up at https://railway.app/
2. **GitHub Repository**: Your code pushed to GitHub
3. **Blockfrost API Key**: Get from https://blockfrost.io/ (free tier available)
4. **Masumi Setup**:
   - Admin Panel: https://masumi-payment-service-production-fe94.up.railway.app/admin/
   - Create API Key and register AI agent
   - Preprod Sokosumi (for testing): https://preprod.sokosumi.com/agents
   - Production Sokosumi: https://app.sokosumi.com/agents
5. **MongoDB Database**: Railway MongoDB or MongoDB Atlas
6. **OpenAI API Key**: For AI analysis (https://platform.openai.com/)
7. **Test ADA (Preprod)**: Get free tADA from https://dispenser.masumi.network/

---

## 🚀 Railway Deployment Steps

### Step 1: Create Railway Project

1. Go to https://railway.app/
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your RiskLens AI repository
5. Railway will auto-detect the Python app

### Step 2: Add MongoDB Service

**Option A: Railway MongoDB (Recommended)**
1. In your Railway project, click **"New"**
2. Select **"Database"** → **"MongoDB"**
3. Railway will create a MongoDB instance
4. Copy the `MONGO_URL` from the MongoDB service variables

**Option B: MongoDB Atlas**
1. Create a cluster at https://www.mongodb.com/cloud/atlas
2. Get your connection string
3. Use it as `MONGO_URL` in Railway

### Step 3: Configure Environment Variables

In Railway, go to your service → **Variables** tab and add:

#### Required Variables

```bash
# Masumi Integration
# Get from: https://masumi-payment-service-production-fe94.up.railway.app/admin/
AGENT_IDENTIFIER=your_agent_identifier_here
PAYMENT_SERVICE_URL=https://masumi-payment-service-production-fe94.up.railway.app/api/v1
PAYMENT_API_KEY=your_masumi_api_key
SELLER_VKEY=your_seller_verification_key
NETWORK=Preprod

# Blockchain Data (from Blockfrost)
BLOCKFROST_PROJECT_ID=preprodxxxxxxxxxxxxxxxxxxxxx

# MongoDB (from Railway MongoDB or Atlas)
MONGO_URL=mongodb://mongo:password@containers-us-west-123.railway.app:7654
MONGO_DB=risklens_ai

# OpenAI (for AI analysis)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

**Important Notes:**
- `NETWORK` must be capitalized: `Preprod` or `Mainnet` (not lowercase)
- `PAYMENT_SERVICE_URL` should point to the Masumi payment service API
- Get API key from Masumi admin panel, not Sokosumi

#### Optional Variables

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# MongoDB Individual Variables (if not using MONGO_URL)
MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_USER=username
MONGO_PASSWORD=password
```

### Step 4: Deploy

1. Railway will automatically deploy after adding variables
2. Wait for deployment to complete (~2-3 minutes)
3. Railway will provide a public URL like:
   ```
   https://your-app-name.up.railway.app
   ```

### Step 5: Verify Deployment

Test your endpoints:

```bash
# Check availability
curl https://your-app-name.up.railway.app/availability

# Expected response:
{
  "status": "available",
  "type": "masumi-agent",
  "agentIdentifier": "your-agent-id",
  "message": "Server operational."
}

# Check input schema
curl https://your-app-name.up.railway.app/input_schema

# Check health
curl https://your-app-name.up.railway.app/health
```

### Step 6: Register Agent with Masumi

**For Testing (Preprod):**
1. Go to https://masumi-payment-service-production-fe94.up.railway.app/admin/
2. Create an API key
3. Register your AI agent with:
   - **Callback URL**: `https://your-app-name.up.railway.app`
   - **Agent Identifier**: Copy the generated identifier
   - **Network**: `Preprod`
   - **Pricing**: Set price (minimum 1 ADA, or use USDM for preprod testing)
4. Copy the `AGENT_IDENTIFIER`, `PAYMENT_API_KEY`, and `SELLER_VKEY`
5. Add them to Railway environment variables

**For Testing Payments:**
- Get free tADA: https://dispenser.masumi.network/
- Test on Preprod Sokosumi: https://preprod.sokosumi.com/agents
- Use credit card `4242 4242 4242 4242` (any CVV, future expiration) for free testing credits

**For Production:**
- Register on: https://app.sokosumi.com/agents
- Use `NETWORK=Mainnet`

- Set real pricing in ADA

---

## 🔍 Verify Blockfrost Integration

After deployment, check Railway logs to confirm Blockfrost is working:

### Good Signs (Real Data):
```
 BLOCKFROST_PROJECT_ID found: preprod1...xyz
 BLOCKFROST API SUCCESSFULLY INITIALIZED!
 Will fetch REAL blockchain data from Cardano preprod
```

### Bad Signs (Mock Data):
```
❌ BLOCKFROST_PROJECT_ID NOT SET!
⚠️  Will use MOCK DATA for all requests
```

If you see mock data warnings, add `BLOCKFROST_PROJECT_ID` to Railway variables.

---

## 📊 Monitoring & Logs

### View Logs in Railway

1. Go to your Railway project
2. Click on your service
3. Click **"Deployments"** tab
4. Click the latest deployment
5. View real-time logs

### What to Look For

**Startup Logs:**
```
INFO - Starting application with configuration:
INFO - PAYMENT_SERVICE_URL: https://api.masumi.network
INFO -  BLOCKFROST API SUCCESSFULLY INITIALIZED!
INFO -  Connected to MongoDB successfully
INFO - Application startup complete
INFO - Uvicorn running on http://0.0.0.0:8000
```

**Request Logs (when agent is used):**
```
INFO - Received start_job request
INFO - 🔍 Fetching address info from Blockfrost
INFO -  REAL BLOCKFROST DATA - First TX: ...
INFO -  Successfully fetched 25 REAL transactions
```

---

## 🔧 Troubleshooting

### Issue 1: Agent Not Showing on Sokosumi

**Symptoms:**
- Agent registered but not visible on marketplace
- `/availability` endpoint works but agent missing

**Solutions:**
1. Verify `AGENT_IDENTIFIER` matches registration
2. Check callback URL is correct Railway URL
3. Test `/availability` returns `agentIdentifier` field
4. Ensure network matches (preprod vs mainnet)

### Issue 2: Mock Data Instead of Real Blockchain Data

**Symptoms:**
- Same results for different wallet addresses
- Logs show "USING MOCK DATA"

**Solutions:**
1. Add `BLOCKFROST_PROJECT_ID` to Railway variables
2. Get free API key from https://blockfrost.io/
3. Ensure `NETWORK` matches Blockfrost project (preprod/mainnet)
4. Redeploy and check logs for "BLOCKFROST API SUCCESSFULLY INITIALIZED"

### Issue 3: MongoDB Connection Errors

**Symptoms:**
- Health check fails
- Logs show "Failed to connect to MongoDB"

**Solutions:**
1. Verify `MONGO_URL` is correct
2. Check MongoDB service is running in Railway
3. Test connection string format:
   ```
   mongodb://user:pass@host:port/database
   ```
4. Ensure MongoDB allows connections from Railway

### Issue 4: 502 Bad Gateway Errors

**Symptoms:**
- All endpoints return 502
- Railway shows app is running

**Solutions:**
1. Check Railway logs for startup errors
2. Verify all required environment variables are set
3. Ensure `API_HOST=0.0.0.0` (not localhost)
4. Check health endpoint: `/health`

### Issue 5: Logs Not Showing

**Symptoms:**
- Only see startup logs, not application logs

**Solutions:**
1. Logs are triggered by requests - make a test request
2. Use `/docs` endpoint to test API
3. Check Railway logs immediately after making request
4. Logs now output to both file and console (already fixed)

---

## 🔄 Updating Your Deployment

### Method 1: Git Push (Automatic)

1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
3. Railway automatically detects and redeploys

### Method 2: Manual Redeploy

1. Go to Railway project
2. Click your service
3. Click **"Deployments"**
4. Click **"Redeploy"** on latest deployment

### Method 3: Environment Variable Change

1. Update variables in Railway
2. Railway automatically redeploys
3. Wait for deployment to complete

---

## 📈 Production Checklist

Before going to production:

- [ ] All environment variables set correctly
- [ ] Blockfrost API key configured (not using mock data)
- [ ] MongoDB connection working
- [ ] Health endpoint returns healthy
- [ ] `/availability` returns correct `agentIdentifier`
- [ ] Test job creation and payment flow
- [ ] Agent visible on Sokosumi marketplace
- [ ] Logs showing real blockchain data
- [ ] Error handling tested
- [ ] Rate limits configured (if needed)

---

## 🎯 Next Steps

After successful deployment:

1. **Test Your Agent**: Create a test job on Sokosumi
2. **Monitor Logs**: Watch Railway logs for any errors
3. **Verify Results**: Check that real blockchain data is being analyzed
4. **Scale if Needed**: Railway auto-scales, but monitor performance
5. **Set Up Alerts**: Configure Railway notifications for errors

---

## 📞 Support & Resources

### Masumi Support

**Community:**
- Telegram: https://t.me/+FtkeBaITmjlkZDky
- Discord: https://discord.gg/WVDHxZQdzp

**Documentation:**
- Masumi Docs: https://docs.masumi.network/
- Installation Guide: https://docs.masumi.network/documentation/get-started/installation
- CrewAI Quickstart: https://github.com/masumi-network/crewai-masumi-quickstart-template

### Testing Resources

- **tADA Faucet**: https://dispenser.masumi.network/
- **Preprod Sokosumi**: https://preprod.sokosumi.com/agents
- **Admin Panel**: https://masumi-payment-service-production-fe94.up.railway.app/admin/

### Troubleshooting

If you encounter issues:

1. Check Railway logs for error messages
2. Verify all environment variables are set (especially `NETWORK=Preprod` with capital P)
3. Test endpoints individually
4. Review this troubleshooting guide
5. Join Masumi community for help

---

**Deployment Platform:** Railway  
**Last Updated:** December 7, 2025  
**Status:** Production Ready
