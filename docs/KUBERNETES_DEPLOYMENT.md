# 🚀 RiskLens AI - Complete Deployment Guide

## Overview
This guide will help you deploy RiskLens AI (Blockchain Compliance & Risk Scoring Agent) to Kubernetes and register it with Masumi.

## Prerequisites

✅ Kubernetes cluster running  
✅ kubectl configured  
✅ Docker installed  
✅ GitHub Container Registry access  
✅ Masumi account with API keys  
✅ OpenAI API key  

## Step 1: Prepare Environment Variables

You need these credentials:

```bash
# Masumi Configuration
PAYMENT_API_KEY="your-masumi-payment-api-key"
AGENT_IDENTIFIER="7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996"
SELLER_VKEY="your-seller-verification-key"

# AI Configuration
OPENAI_API_KEY="your-openai-api-key"

# Network
NETWORK="Preprod"  # or "Mainnet"
```

## Step 2: Create Kubernetes Secrets

```bash
kubectl create secret generic masumi-secrets \
  --from-literal=payment_api_key='YOUR_PAYMENT_API_KEY' \
  --from-literal=agent_identifier='7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996' \
  --from-literal=seller_vkey='YOUR_SELLER_VKEY' \
  --from-literal=openai_api_key='YOUR_OPENAI_API_KEY'

# Verify secrets
kubectl get secret masumi-secrets
```

## Step 3: Build and Push Docker Image

```bash
# Build the image
docker build -t ghcr.io/vinaycharlie01/local-llama-agent-python:v1 .

# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u vinaycharlie01 --password-stdin

# Push the image
docker push ghcr.io/vinaycharlie01/local-llama-agent-python:v1
```

## Step 4: Deploy to Kubernetes

```bash
# Apply the deployment
kubectl apply -f deploy.yaml

# Check deployment status
kubectl get deployments
kubectl get pods -l app=python-api

# Wait for pod to be ready
kubectl wait --for=condition=ready pod -l app=python-api --timeout=300s
```

## Step 5: Verify Deployment

```bash
# Check pod logs
kubectl logs -f deployment/python-api

# Check service
kubectl get svc python-api

# Check ingress
kubectl get ingress python-api-ingress
```

## Step 6: Test the Agent

### Test Availability Endpoint
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

### Test Input Schema
```bash
curl http://161.156.165.133.nip.io/input_schema
```

**Expected Response:**
```json
{
  "input_data": [
    {
      "id": "wallet_address",
      "type": "string",
      "name": "Wallet Address",
      "data": {
        "description": "The blockchain wallet address to analyze for compliance and risk assessment",
        "placeholder": "Enter wallet address (e.g., 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb)"
      }
    }
  ]
}
```

### Test Risk Analysis (Full Flow)
```bash
# Start a risk analysis job
curl -X POST http://161.156.165.133.nip.io/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "test_user_001",
    "input_data": {
      "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    }
  }'

# Save the job_id from response, then check status
curl "http://161.156.165.133.nip.io/status?job_id=YOUR_JOB_ID"
```

## Step 7: Register with Masumi

### Option A: Using Registration Script
```bash
pip install requests
python register_agent.py
```

### Option B: Manual Registration via API
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

### Option C: Via Masumi Dashboard
1. Login to Masumi dashboard
2. Navigate to "Agents" or "Register Agent"
3. Fill in:
   - **Agent Identifier**: `7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996`
   - **Agent URL**: `http://161.156.165.133.nip.io`
   - **Seller VKey**: Your verification key
   - **Network**: `Preprod`
4. Submit registration

## Step 8: Verify Registration in Masumi

After registration, check:

1. **Masumi Dashboard** → Look for your agent in the agents list
2. **Agent Status** → Should show as "Available" or "Online"
3. **Test Transaction** → Try creating a job through Masumi interface

## Monitoring & Maintenance

### View Logs
```bash
# Real-time logs
kubectl logs -f deployment/python-api

# Last 100 lines
kubectl logs deployment/python-api --tail=100

# Logs from specific pod
kubectl logs python-api-867497c998-77ztv
```

### Check Resource Usage
```bash
kubectl top pods -l app=python-api
kubectl describe pod -l app=python-api
```

### Update Deployment
```bash
# After code changes
docker build -t ghcr.io/vinaycharlie01/local-llama-agent-python:v1 .
docker push ghcr.io/vinaycharlie01/local-llama-agent-python:v1
kubectl rollout restart deployment/python-api
kubectl rollout status deployment/python-api
```

### Scale Deployment
```bash
# Scale to 3 replicas
kubectl scale deployment python-api --replicas=3

# Check scaling
kubectl get pods -l app=python-api
```

## Troubleshooting

### Pod Not Starting
```bash
# Check pod status
kubectl describe pod -l app=python-api

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check logs
kubectl logs deployment/python-api
```

### Agent Not Showing in Masumi
1. Verify agent is accessible: `curl http://161.156.165.133.nip.io/availability`
2. Check if agentIdentifier is returned in response
3. Verify registration was successful
4. Check Masumi dashboard for agent status
5. Contact Masumi support if needed

### Payment Issues
```bash
# Check payment service connectivity
kubectl exec -it deployment/python-api -- curl https://masumi-payment-service-production-755f.up.railway.app/api/v1/health

# Verify API key
kubectl get secret masumi-secrets -o jsonpath='{.data.payment_api_key}' | base64 -d
```

### OpenAI API Errors
```bash
# Check OpenAI key
kubectl get secret masumi-secrets -o jsonpath='{.data.openai_api_key}' | base64 -d

# Check logs for API errors
kubectl logs deployment/python-api | grep -i "openai\|error"
```

## Performance Optimization

### Increase Resources
Edit `deploy.yaml`:
```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

### Enable Caching
Add Redis for caching analysis results (future enhancement)

### Load Balancing
Increase replicas for high traffic:
```bash
kubectl scale deployment python-api --replicas=5
```

## Security Best Practices

1. **Rotate Secrets Regularly**
   ```bash
   kubectl delete secret masumi-secrets
   kubectl create secret generic masumi-secrets --from-literal=...
   kubectl rollout restart deployment/python-api
   ```

2. **Use HTTPS**
   - Ensure TLS certificate is valid
   - Check cert-manager is working

3. **Monitor Access Logs**
   ```bash
   kubectl logs -n ingress-nginx deployment/ingress-nginx-controller
   ```

4. **Set Resource Limits**
   - Prevent resource exhaustion
   - Configure proper limits in deploy.yaml

## Backup & Recovery

### Backup Configuration
```bash
kubectl get deployment python-api -o yaml > backup-deployment.yaml
kubectl get service python-api -o yaml > backup-service.yaml
kubectl get ingress python-api-ingress -o yaml > backup-ingress.yaml
```

### Restore from Backup
```bash
kubectl apply -f backup-deployment.yaml
kubectl apply -f backup-service.yaml
kubectl apply -f backup-ingress.yaml
```

## Production Checklist

- [ ] All secrets configured correctly
- [ ] Docker image built and pushed
- [ ] Deployment applied to Kubernetes
- [ ] Pods running and healthy
- [ ] Ingress configured with valid domain
- [ ] TLS certificate issued
- [ ] Agent registered with Masumi
- [ ] Agent visible in Masumi dashboard
- [ ] Test job completed successfully
- [ ] Monitoring and logging configured
- [ ] Resource limits set appropriately
- [ ] Backup strategy in place

## Support

For issues or questions:
- Check logs: `kubectl logs deployment/python-api`
- Review documentation: `README.md`
- Contact Team X07
- Masumi support: [support link]

---

**RiskLens AI - Built by Team X07 for Masumi Hackathon** 🛡️

// Made with Bob
