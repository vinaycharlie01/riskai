# 📡 RiskLens AI - API Reference

Complete API documentation for RiskLens AI blockchain compliance and risk scoring agent.

**Base URL:** `https://your-app.up.railway.app` or `http://localhost:8000`  
**API Version:** 1.0.0  
**Protocol:** REST (MIP-003 Compliant)  
**Format:** JSON

---

## 📋 Table of Contents

1. [MIP-003 Compliance](#mip-003-compliance)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)
6. [Examples](#examples)

---

## 🔐 MIP-003 Compliance

RiskLens AI implements the **Masumi Integration Protocol (MIP-003)** standard, which defines required endpoints for Masumi Network agents.

### Required Endpoints

- ✅ `GET /availability` - Agent availability status
- ✅ `GET /input_schema` - Input requirements
- ✅ `POST /start_job` - Create job and payment request
- ✅ `GET /status` - Check job status

### Additional Endpoints

- ✅ `GET /` - API information
- ✅ `GET /health` - Health check with MongoDB ping

---

## 🔐 Authentication

RiskLens AI uses **Masumi Network payment-based authentication**. No API keys required for public endpoints.

### Payment Flow

1. Submit job via `/start_job`
2. Receive payment details (blockchain identifier)
3. Complete payment on Masumi Network
4. Analysis starts automatically after payment confirmation
5. Retrieve results via `/status`

---

## 🎯 Endpoints

### 1. Root Endpoint

Get API information and available endpoints.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "RiskLens AI - Blockchain Compliance & Risk Scoring Agent",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoints": {
    "availability": "/availability",
    "input_schema": "/input_schema",
    "start_job": "/start_job",
    "status": "/status?job_id=<job_id>",
    "health": "/health"
  }
}
```

**Status Codes:**
- `200 OK` - Success

**Example:**
```bash
curl https://your-app.up.railway.app/
```

---

### 2. Health Check

Check if the API server and MongoDB are operational.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK` - Server and MongoDB are healthy
- `503 Service Unavailable` - MongoDB connection failed

**Example:**
```bash
curl https://your-app.up.railway.app/health
```

---

### 3. Check Availability (MIP-003)

Verify agent availability and get agent information.

**Endpoint:** `GET /availability`

**Response:**
```json
{
  "status": "available",
  "type": "masumi-agent",
  "agentIdentifier": "your-agent-identifier",
  "message": "Server operational."
}
```

**Fields:**
- `status` - Always "available" if agent is running
- `type` - Always "masumi-agent" for MIP-003 compliance
- `agentIdentifier` - Unique agent identifier from Masumi registration
- `message` - Human-readable status message

**Status Codes:**
- `200 OK` - Agent is available
- `500 Internal Server Error` - Agent not configured (AGENT_IDENTIFIER missing)

**Example:**
```bash
curl https://your-app.up.railway.app/availability
```

---

### 4. Get Input Schema (MIP-003)

Retrieve the expected input format for job submission.

**Endpoint:** `GET /input_schema`

**Response:**
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

**Status Codes:**
- `200 OK` - Schema retrieved successfully

**Example:**
```bash
curl https://your-app.up.railway.app/input_schema
```

---

### 5. Start Risk Analysis Job (MIP-003)

Submit a wallet address for risk analysis and create a payment request.

**Endpoint:** `POST /start_job`

**Request Body:**
```json
{
  "identifier_from_purchaser": "string",
  "input_data": {
    "wallet_address": "string"
  }
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `identifier_from_purchaser` | string | Yes | Unique identifier from the client (e.g., "user_123", "kyc_check_001") |
| `input_data.wallet_address` | string | Yes | Cardano wallet address to analyze (addr_test1... or addr1...) |

**Response:**
```json
{
  "status": "success",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "blockchainIdentifier": "payment_abc123",
  "submitResultTime": 1733567890,
  "unlockTime": 1733571490,
  "externalDisputeUnlockTime": 1733575090,
  "agentIdentifier": "your-agent-identifier",
  "sellerVKey": "vkey1...",
  "identifierFromPurchaser": "user_123",
  "input_hash": "hash_of_input_data",
  "payByTime": 1733569690
}
```

**Response Fields:**
- `job_id` - Unique job identifier for status checks
- `blockchainIdentifier` - Payment identifier on Masumi Network
- `submitResultTime` - Unix timestamp when result must be submitted
- `unlockTime` - Unix timestamp when payment unlocks
- `externalDisputeUnlockTime` - Unix timestamp for dispute resolution
- `payByTime` - Unix timestamp deadline for payment

**Status Codes:**
- `200 OK` - Job created successfully
- `400 Bad Request` - Invalid input data or missing fields
- `500 Internal Server Error` - Server error

**Example:**
```bash
curl -X POST https://your-app.up.railway.app/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "exchange_kyc_001",
    "input_data": {
      "wallet_address": "addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgs68faae"
    }
  }'
```

---

### 6. Check Job Status (MIP-003)

Retrieve the current status and results of a job.

**Endpoint:** `GET /status`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | string | Yes | The job ID returned from `/start_job` |

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "payment_status": "result_submitted",
  "result": "🔍 BLOCKCHAIN WALLET RISK ANALYSIS REPORT\n\n📍 Wallet Address: addr_test1...\n📅 Analysis Date: 2025-12-07T10:30:00Z\n\n📊 RISK ASSESSMENT\n   Risk Score: 25/100\n   Risk Category: Low Risk\n   Trust Score: 75/100\n   Compliance Status: Compliant\n   Confidence Level: High\n\n📋 EXECUTIVE SUMMARY\nThis wallet shows normal activity patterns with no significant red flags...\n\n💰 TRANSACTION SUMMARY\n   Total Transactions: 150\n   Total Volume: 500 ADA\n   Active Period: 180 days\n   Counterparties: 45\n\n⚠️  RISK FACTORS\n\n1. Transaction Frequency\n   Severity: Low\n   Description: Normal transaction frequency observed\n   Impact: Minimal impact on risk score\n\n🚨 SUSPICIOUS ACTIVITIES\n   No suspicious activities detected.\n\n💡 RECOMMENDATIONS\n1. Wallet shows normal behavior patterns\n2. No immediate concerns identified\n3. Continue standard monitoring\n\n🔐 VERIFICATION\n   Report Hash: 0xabc123...\n\nEnd of Report\n\n🌐 Learn more about RiskLens AI:\n   https://studio--studio-2671206846-b156f.us-central1.hosted.app/\n"
}
```

**Job Status Values:**

| Status | Description |
|--------|-------------|
| `awaiting_payment` | Waiting for payment to be completed |
| `running` | Analysis in progress |
| `completed` | Analysis finished, results available |
| `failed` | Analysis failed, check error field |

**Payment Status Values:**

| Status | Description |
|--------|-------------|
| `pending` | Payment not yet received |
| `paid` | Payment confirmed, analysis starting |
| `result_submitted` | Result submitted to Masumi Network |
| `unknown` | Payment status unclear |
| `error` | Payment check failed |

**Result Format:**
- Results are returned as a **formatted string** (not JSON)
- Designed for display on Sokosumi dashboard
- Includes wallet address, risk scores, analysis, and recommendations
- Contains website link at the end

**Status Codes:**
- `200 OK` - Status retrieved successfully
- `404 Not Found` - Job ID not found

**Example:**
```bash
curl "https://your-app.up.railway.app/status?job_id=550e8400-e29b-41d4-a716-446655440000"
```

---

## 📊 Data Models

### Risk Analysis Result

The result is a formatted string containing:

```
🔍 BLOCKCHAIN WALLET RISK ANALYSIS REPORT

📍 Wallet Address: [address]
📅 Analysis Date: [timestamp]

📊 RISK ASSESSMENT
   Risk Score: [0-100]/100
   Risk Category: [Low/Medium/High/Critical]
   Trust Score: [0-100]/100
   Compliance Status: [Compliant/Non-Compliant/Requires Review]
   Confidence Level: [High/Medium/Low]

📋 EXECUTIVE SUMMARY
[Brief overview of findings]

💰 TRANSACTION SUMMARY
   Total Transactions: [number]
   Total Volume: [amount] ADA
   Active Period: [duration]
   Counterparties: [number]

⚠️  RISK FACTORS
[List of identified risk factors with severity and impact]

🚨 SUSPICIOUS ACTIVITIES
[List of suspicious activities or "No suspicious activities detected"]

💡 RECOMMENDATIONS
[List of actionable recommendations]

🔐 VERIFICATION
   Report Hash: [hash for on-chain verification]

End of Report

🌐 Learn more about RiskLens AI:
   [website URL]
```

### Risk Score Categories

| Score Range | Category | Description |
|-------------|----------|-------------|
| 0-20 | Low Risk | Normal behavior, minimal concerns |
| 21-50 | Medium Risk | Some concerns, requires monitoring |
| 51-75 | High Risk | Significant concerns, enhanced due diligence |
| 76-100 | Critical Risk | Severe concerns, immediate action required |

---

## ⚠️ Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

| Status Code | Description | Common Causes |
|-------------|-------------|---------------|
| `400 Bad Request` | Invalid input | Missing fields, invalid wallet address format |
| `404 Not Found` | Resource not found | Invalid job_id |
| `500 Internal Server Error` | Server error | Missing configuration, database error |
| `503 Service Unavailable` | Service unavailable | MongoDB connection failed |

### Example Error Response

```json
{
  "detail": "Bad Request: If input_data or identifier_from_purchaser is missing, invalid, or does not adhere to the schema."
}
```

---

## 💻 Complete Workflow Example

```bash
# 1. Check health
curl https://your-app.up.railway.app/health

# 2. Check availability
curl https://your-app.up.railway.app/availability

# 3. Get input schema
curl https://your-app.up.railway.app/input_schema

# 4. Start job and save response
JOB_RESPONSE=$(curl -s -X POST https://your-app.up.railway.app/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "test_001",
    "input_data": {
      "wallet_address": "addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgs68faae"
    }
  }')

# Extract job_id
JOB_ID=$(echo $JOB_RESPONSE | jq -r '.job_id')
echo "Job ID: $JOB_ID"

# 5. Complete payment on Masumi Network (external step)
# ... use blockchainIdentifier from response ...

# 6. Check status (repeat until completed)
curl "https://your-app.up.railway.app/status?job_id=$JOB_ID"
```

---

## 🔗 Related Documentation

- [Quick Start Guide](QUICK_START.md) - Get started quickly
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Deploy to Railway
- [How It Works](HOW_IT_WORKS.md) - Understand the system
- [Masumi Integration](MASUMI_INTEGRATION.md) - Payment protocol details

---

## 📞 Support

Need help with the API?

- 📖 Check [Deployment Guide](DEPLOYMENT_GUIDE.md) for troubleshooting
- 📚 Review [Workflow Documentation](WORKFLOW_DOCUMENTATION.md)
- 💬 Masumi docs: https://docs.masumi.network/

---

**Last Updated:** December 7, 2025  
**API Version:** 1.0.0  
**Protocol:** MIP-003 Compliant

---

**Built for Cardano Blockchain Compliance & Risk Assessment**