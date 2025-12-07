# 🔧 Fix for Masumi Agent Registration Issue

## Problem Identified
Your agent was running but **not showing up in Masumi** because the `/availability` endpoint was not returning the `agentIdentifier` field, which is required for Masumi to recognize and register your agent.

## What Was Fixed
Updated the `/availability` endpoint in `main.py` to include the `agentIdentifier` field.

## Deployment Steps

### Step 1: Build and Push Docker Image
```bash
# Build the new image
docker build -t ghcr.io/vinaycharlie01/local-llama-agent-python:v1 .

# Push to registry
docker push ghcr.io/vinaycharlie01/local-llama-agent-python:v1
```

### Step 2: Restart Kubernetes Deployment
```bash
# Force restart to pull the new image
kubectl rollout restart deployment/python-api

# Wait for rollout to complete
kubectl rollout status deployment/python-api

# Check pod status
kubectl get pods -l app=python-api
```

### Step 3: Verify the Fix
```bash
# Check the new pod logs
kubectl logs -f deployment/python-api

# Test the availability endpoint
curl http://161.156.165.133.nip.io/availability
```

**Expected Response:**
```json
{
  "status": "available",
  "type": "masumi-agent",
  "agentIdentifier": "your-agent-identifier-here",
  "message": "Server operational."
}
```

### Step 4: Verify in Masumi
1. Go to your Masumi dashboard
2. Check the agents list
3. Your agent should now appear with the correct identifier

## Quick Deploy Script
You can also use the provided script:
```bash
chmod +x redeploy.sh
./redeploy.sh
```

## Troubleshooting

### If agent still doesn't show up:
1. **Check AGENT_IDENTIFIER is set:**
   ```bash
   kubectl get secret masumi-secrets -o jsonpath='{.data.agent_identifier}' | base64 -d
   ```

2. **Check pod logs for errors:**
   ```bash
   kubectl logs deployment/python-api --tail=50
   ```

3. **Verify the availability endpoint:**
   ```bash
   kubectl exec -it deployment/python-api -- curl localhost:8000/availability
   ```

4. **Check if Masumi can reach your endpoint:**
   - Ensure your ingress is working: `curl http://161.156.165.133.nip.io/availability`
   - Check ingress logs: `kubectl logs -n ingress-nginx deployment/ingress-nginx-controller`

### If you see "Agent identifier not configured" error:
The AGENT_IDENTIFIER secret is missing or empty. Set it:
```bash
kubectl create secret generic masumi-secrets \
  --from-literal=agent_identifier='your-agent-id' \
  --from-literal=payment_api_key='your-api-key' \
  --from-literal=seller_vkey='your-vkey' \
  --from-literal=openai_api_key='your-openai-key' \
  --dry-run=client -o yaml | kubectl apply -f -
```

## What Changed in the Code

**Before:**
```python
@app.get("/availability")
async def check_availability():
    return {"status": "available", "type": "masumi-agent", "message": "Server operational."}
```

**After:**
```python
@app.get("/availability")
async def check_availability():
    agent_identifier = os.getenv("AGENT_IDENTIFIER")
    
    if not agent_identifier:
        logger.error("AGENT_IDENTIFIER environment variable is not set!")
        raise HTTPException(status_code=500, detail="Agent identifier not configured")
    
    logger.info(f"Availability check - Agent Identifier: {agent_identifier}")
    return {
        "status": "available",
        "type": "masumi-agent",
        "agentIdentifier": agent_identifier,
        "message": "Server operational."
    }
```

## Next Steps After Deployment
1. Monitor the logs to ensure no errors
2. Test creating a job through Masumi
3. Verify payment flow works correctly

---
**Note:** The `agentIdentifier` field is **required** by Masumi to register and track agents. Without it, Masumi cannot identify your agent even if it's running and healthy.


