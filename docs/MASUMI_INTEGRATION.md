# 🎯 Masumi Agent Registration Guide

## Problem
Your agent is deployed and running, but **not showing in Masumi/Suksumi** because it needs to be **manually registered**.

## Solution: Register Your Agent

### Option 1: Using the Registration Script (Recommended)

1. **Install required package:**
   ```bash
   pip install requests
   ```

2. **Run the registration script:**
   ```bash
   python register_agent.py
   ```

3. **Follow the prompts** - The script will:
   - Verify your agent is accessible
   - Register it with Masumi
   - Confirm successful registration

### Option 2: Manual Registration via API

If the script doesn't work, register manually:

```bash
# Get your environment variables
PAYMENT_API_KEY="your-api-key"
AGENT_IDENTIFIER="7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996"
SELLER_VKEY="your-seller-vkey"
AGENT_URL="http://{{Domain}}/"

# Register the agent
curl -X POST "https://masumi-payment-service-production-755f.up.railway.app/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYMENT_API_KEY" \
  -d '{
    "agentIdentifier": "'"$AGENT_IDENTIFIER"'",
    "agentUrl": "'"$AGENT_URL"'",
    "sellerVKey": "'"$SELLER_VKEY"'",
    "network": "Preprod"
  }'
```

### Option 3: Register via Masumi Dashboard

1. **Go to Masumi Dashboard:**
   - Visit: https://masumi.ai (or your Masumi instance URL)
   - Login with your credentials

2. **Navigate to Agents Section:**
   - Look for "Agents", "My Agents", or "Register Agent"

3. **Fill in Agent Details:**
   - **Agent Identifier:** `7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996`
   - **Agent URL:** `https://{{Domain}}`
   - **Seller VKey:** (from your secrets)
   - **Network:** `Preprod`

4. **Submit Registration**

## Verification Steps

After registration, verify your agent appears:

### 1. Check Agent Availability
```bash
curl https://{{Domain}}/availability
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

### 2. Check Input Schema
```bash
curl http://161.156.165.133.nip.io/input_schema
```

### 3. Check Masumi Dashboard
- Login to Masumi
- Navigate to Agents list
- Look for your agent identifier

## Common Issues & Solutions

### Issue 1: "Agent not found" in Masumi
**Solution:** The agent needs to be registered first. Use the registration script or manual API call.

### Issue 2: "Agent URL not accessible"
**Solution:** 
- Verify ingress is working: `kubectl get ingress`
- Test from outside: `curl http://161.156.165.133.nip.io/availability`
- Check firewall rules

### Issue 3: "Invalid API Key"
**Solution:**
```bash
# Verify your API key
kubectl get secret masumi-secrets -o jsonpath='{.data.payment_api_key}' | base64 -d
```

### Issue 4: "Agent Identifier mismatch"
**Solution:** Ensure the identifier in your registration matches the one returned by `/availability`

## Environment Variables Needed

Make sure these are set in your Kubernetes secrets:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: masumi-secrets
type: Opaque
stringData:
  payment_api_key: "your-masumi-api-key"
  agent_identifier: "7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996"
  seller_vkey: "your-seller-verification-key"
  openai_api_key: "your-openai-api-key"
```

## Testing Your Registered Agent

Once registered, test the full workflow:

```bash
# 1. Start a job
curl -X POST "http://161.156.165.133.nip.io/start_job" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "test-user-123",
    "input_data": {
      "text": "Write a short story about AI"
    }
  }'

# 2. Check job status (use job_id from response)
curl "http://161.156.165.133.nip.io/status?job_id=YOUR_JOB_ID"
```

## Where to Find Your Agent in Masumi

After successful registration, your agent should appear in:

1. **Masumi Dashboard** → **Agents** section
2. **Agent Marketplace** (if public)
3. **My Agents** or **Registered Agents** page

Look for:
- **Agent ID:** `7e8bdaf2b2b919a3a4b94002cafb50086c0c845fe535d07a77ab7f775f39dd22a4b6c8e6e2b4e01316b52eb4926e501d5d1a9a3fe3c0e1f7ee24a996`
- **Status:** Available/Online
- **URL:** `http://161.156.165.133.nip.io`

## Need Help?

If you're still having issues:

1. **Check Masumi Documentation:** Look for agent registration requirements
2. **Contact Masumi Support:** Provide your agent identifier
3. **Check Logs:** `kubectl logs deployment/python-api`
4. **Verify Network:** Ensure Masumi can reach your agent URL

---

**Important:** The agent must be **publicly accessible** for Masumi to register and use it. Make sure your ingress and firewall allow external access.


