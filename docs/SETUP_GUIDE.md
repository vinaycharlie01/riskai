# 🛡️ RiskLens AI - Complete Setup Guide

## Overview
This guide will help you set up RiskLens AI with real blockchain data integration using Blockfrost API.

## Prerequisites

### Required Accounts
1. **Masumi Account** - For agent registration and payments
2. **OpenAI Account** - For AI capabilities
3. **Blockfrost Account** - For blockchain data (https://blockfrost.io)
4. **GitHub Account** - For container registry
5. **Kubernetes Cluster** - For deployment

## Step 1: Get API Keys

### 1.1 Blockfrost API Key
1. Go to https://blockfrost.io
2. Sign up for a free account
3. Create a new project
4. Select network: **Cardano Preprod** (for testing) or **Mainnet** (for production)
5. Copy your **Project ID** (starts with `preprod...` or `mainnet...`)

### 1.2 OpenAI API Key
1. Go to https://platform.openai.com
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy and save it securely

### 1.3 Masumi API Keys
1. Log in to Masumi dashboard
2. Navigate to API settings
3. Generate/copy:
   - Payment API Key
   - Agent Identifier
   - Seller VKey

## Step 2: Configure Kubernetes Secrets

Create a secret with all required credentials:

```bash
kubectl create secret generic masumi-secrets \
  --from-literal=payment_api_key='YOUR_MASUMI_PAYMENT_API_KEY' \
  --from-literal=agent_identifier='7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996' \
  --from-literal=seller_vkey='YOUR_SELLER_VKEY' \
  --from-literal=openai_api_key='YOUR_OPENAI_API_KEY' \
  --from-literal=blockfrost_project_id='YOUR_BLOCKFROST_PROJECT_ID'
```

**Example with real values:**
```bash
kubectl create secret generic masumi-secrets \
  --from-literal=payment_api_key='msk_live_abc123...' \
  --from-literal=agent_identifier='7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996' \
  --from-literal=seller_vkey='vkey1abc123...' \
  --from-literal=openai_api_key='sk-proj-abc123...' \
  --from-literal=blockfrost_project_id='preprodABC123XYZ...'
```

### Verify Secrets
```bash
# List secrets
kubectl get secrets

# Check secret contents (base64 encoded)
kubectl get secret masumi-secrets -o yaml

# Decode a specific key
kubectl get secret masumi-secrets -o jsonpath='{.data.blockfrost_project_id}' | base64 -d
```

## Step 3: Local Development Setup

### 3.1 Clone Repository
```bash
git clone <your-repo-url>
cd riskai
```

### 3.2 Create Virtual Environment
```bash
# Create virtual environment using python3
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

**Important:** Always activate the virtual environment before working on the project:
```bash
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

### 3.3 Install Dependencies
```bash
# Make sure virtual environment is activated (you should see (.venv) in your prompt)
pip install -r requirements.txt
```

### 3.4 Create .env File
```bash
cat > .env << EOF
# Masumi Configuration
PAYMENT_SERVICE_URL=https://masumi-payment-service-production-755f.up.railway.app/api/v1
PAYMENT_API_KEY=your_masumi_payment_api_key
AGENT_IDENTIFIER=7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996
SELLER_VKEY=your_seller_vkey
NETWORK=Preprod

# Payment Configuration
PAYMENT_AMOUNT=1000000
PAYMENT_UNIT=16a55b2a349361ff88c03788f93e1e966e5d689605d044fef722ddde0014df10745553444d

# AI Configuration
OPENAI_API_KEY=your_openai_api_key

# Blockchain Configuration
BLOCKFROST_PROJECT_ID=your_blockfrost_project_id

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
EOF
```

### 3.5 Test Locally
```bash
# Test standalone mode
python main.py

# Test API mode
python main.py api
```

## Step 4: Docker Build

### 4.1 Build Image
```bash
docker build -t ghcr.io/vinaycharlie01/local-llama-agent-python:v1 .
```

### 4.2 Test Docker Image Locally
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="your-key" \
  -e PAYMENT_API_KEY="your-key" \
  -e AGENT_IDENTIFIER="your-id" \
  -e SELLER_VKEY="your-vkey" \
  -e BLOCKFROST_PROJECT_ID="your-project-id" \
  ghcr.io/vinaycharlie01/local-llama-agent-python:v1
```

### 4.3 Push to Registry
```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u vinaycharlie01 --password-stdin

# Push image
docker push ghcr.io/vinaycharlie01/local-llama-agent-python:v1
```

## Step 5: Deploy to Kubernetes

### 5.1 Apply Deployment
```bash
kubectl apply -f deploy.yaml
```

### 5.2 Check Deployment Status
```bash
# Check pods
kubectl get pods -l app=python-api

# Check deployment
kubectl get deployment python-api

# Check service
kubectl get svc python-api

# Check ingress
kubectl get ingress python-api-ingress
```

### 5.3 View Logs
```bash
# Real-time logs
kubectl logs -f deployment/python-api

# Last 100 lines
kubectl logs deployment/python-api --tail=100
```

## Step 6: Test the Agent

### 6.1 Test Availability
```bash
curl http://161.156.165.133.nip.io/availability
```

**Expected Response:**
```json
{
  "status": "available",
  "type": "masumi-agent",
  "agentIdentifier": "7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996",
  "version": "1.0.0",
  "message": "Server operational."
}
```

### 6.2 Test Input Schema
```bash
curl http://161.156.165.133.nip.io/input_schema
```

### 6.3 Test Risk Analysis

**Using a real Cardano address:**
```bash
curl -X POST http://161.156.165.133.nip.io/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "test_user_001",
    "input_data": {
      "wallet_address": "addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj83ws8lhrn648jjxtwq2ytjqp"
    }
  }'
```

**Check job status:**
```bash
curl "http://161.156.165.133.nip.io/status?job_id=YOUR_JOB_ID"
```

## Step 7: Register with Masumi

### Option A: Using Script
```bash
python register_agent.py
```

### Option B: Manual Registration
```bash
curl -X POST "https://masumi-payment-service-production-755f.up.railway.app/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_PAYMENT_API_KEY" \
  -d '{
    "agentIdentifier": "7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996",
    "agentUrl": "http://161.156.165.133.nip.io",
    "sellerVKey": "YOUR_SELLER_VKEY",
    "network": "Preprod"
  }'
```

## Step 8: Verify in Masumi Dashboard

1. Log in to Masumi dashboard
2. Navigate to "Agents" section
3. Look for your agent with identifier: `7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996`
4. Status should show as "Available" or "Online"

## Troubleshooting

### Issue: Blockfrost API Errors

**Check Project ID:**
```bash
kubectl get secret masumi-secrets -o jsonpath='{.data.blockfrost_project_id}' | base64 -d
```

**Verify in logs:**
```bash
kubectl logs deployment/python-api | grep -i blockfrost
```

**Solution:**
- Ensure Project ID is correct
- Check network matches (preprod vs mainnet)
- Verify Blockfrost account is active

### Issue: OpenAI API Errors

**Check logs:**
```bash
kubectl logs deployment/python-api | grep -i openai
```

**Solution:**
- Verify API key is valid
- Check OpenAI account has credits
- Ensure API key has correct permissions

### Issue: Agent Not in Masumi

**Verify registration:**
```bash
curl http://161.156.165.133.nip.io/availability
```

**Solution:**
- Ensure agentIdentifier is returned
- Re-run registration script
- Check Masumi admin portal
- Verify agent URL is accessible from internet

### Issue: Pod Crashes

**Check pod status:**
```bash
kubectl describe pod -l app=python-api
```

**Check logs:**
```bash
kubectl logs deployment/python-api --previous
```

**Common causes:**
- Missing secrets
- Invalid API keys
- Out of memory
- Image pull errors

## Quick Commands Reference

```bash
# View all resources
kubectl get all -l app=python-api

# Restart deployment
kubectl rollout restart deployment/python-api

# Scale deployment
kubectl scale deployment python-api --replicas=3

# Update secrets
kubectl delete secret masumi-secrets
kubectl create secret generic masumi-secrets --from-literal=...

# Force redeploy
kubectl rollout restart deployment/python-api

# Check resource usage
kubectl top pods -l app=python-api

# Port forward for local testing
kubectl port-forward deployment/python-api 8000:8000
```

## Production Checklist

- [ ] All API keys configured
- [ ] Blockfrost Project ID set (correct network)
- [ ] Secrets created in Kubernetes
- [ ] Docker image built and pushed
- [ ] Deployment applied
- [ ] Pods running and healthy
- [ ] Ingress configured with valid domain
- [ ] TLS certificate issued
- [ ] Agent accessible from internet
- [ ] Agent registered with Masumi
- [ ] Agent visible in Masumi dashboard
- [ ] Test analysis completed successfully
- [ ] Monitoring configured
- [ ] Backup strategy in place

## Support

For issues:
- Check logs: `kubectl logs deployment/python-api`
- Review documentation
- Contact Team X07
- Blockfrost support: https://blockfrost.io/support
- Masumi support: [support link]

---

**RiskLens AI - Built by Team X07** 🛡️


