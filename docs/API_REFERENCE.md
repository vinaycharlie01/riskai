# 📡 RiskLens AI - API Reference

Complete API documentation for RiskLens AI blockchain compliance and risk scoring agent.

**Base URL:** `http://your-domain:8000`  
**API Version:** 1.0.0  
**Protocol:** REST  
**Format:** JSON

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Data Models](#data-models)
4. [Error Handling](#error-handling)
5. [Rate Limits](#rate-limits)
6. [Examples](#examples)

---

## 🔐 Authentication

Currently, RiskLens AI uses **Masumi Network payment-based authentication**. No API keys required for public endpoints.

### Payment Flow
1. Submit job via `/start_job`
2. Receive payment details
3. Complete payment on Masumi Network
4. Analysis starts automatically
5. Retrieve results via `/status`

---

## 🎯 Endpoints

### 1. Health Check

Check if the API server is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK` - Server is healthy

**Example:**
```bash
curl http://localhost:8000/health
```

---

### 2. Check Availability

Verify agent availability and get agent information.

**Endpoint:** `GET /availability`

**Response:**
```json
{
  "status": "available",
  "type": "masumi-agent",
  "agentIdentifier": "risklens-ai-v1",
  "message": "Server operational."
}
```

**Status Codes:**
- `200 OK` - Agent is available
- `500 Internal Server Error` - Agent not configured

**Example:**
```bash
curl http://localhost:8000/availability
```

---

### 3. Get Input Schema

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
curl http://localhost:8000/input_schema
```

---

### 4. Start Risk Analysis Job

Submit a wallet address for risk analysis.

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
| `input_data.wallet_address` | string | Yes | Blockchain wallet address to analyze |

**Response:**
```json
{
  "status": "success",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "blockchainIdentifier": "payment_abc123",
  "submitResultTime": "2025-11-29T15:00:00Z",
  "unlockTime": "2025-11-29T16:00:00Z",
  "externalDisputeUnlockTime": "2025-11-29T17:00:00Z",
  "agentIdentifier": "risklens-ai-v1",
  "sellerVKey": "vkey1...",
  "identifierFromPurchaser": "user_123",
  "amounts": [
    {
      "amount": "10000000",
      "unit": "lovelace"
    }
  ],
  "input_hash": "hash_of_input_data",
  "payByTime": "2025-11-29T15:30:00Z"
}
```

**Status Codes:**
- `200 OK` - Job created successfully
- `400 Bad Request` - Invalid input data
- `500 Internal Server Error` - Server error

**Example:**
```bash
curl -X POST http://localhost:8000/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "exchange_kyc_001",
    "input_data": {
      "wallet_address": "addr_test1q"
    }
  }'
```

---

### 5. Check Job Status

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
  "payment_status": "completed",
  "result": {
    "wallet_address": "addr_test1...",
    "analysis_timestamp": "2025-11-29T15:05:00Z",
    "risk_score": 25,
    "risk_category": "Low Risk",
    "trust_score": 75,
    "executive_summary": "This wallet shows normal activity patterns...",
    "transaction_summary": {
      "total_transactions": 150,
      "total_volume": "500000 ADA",
      "active_period": "180 days",
      "counterparties": 45
    },
    "risk_factors": [
      {
        "factor": "Transaction Frequency",
        "severity": "Low",
        "description": "Normal transaction frequency observed",
        "impact": "Minimal impact on risk score"
      }
    ],
    "suspicious_activities": [],
    "recommendations": [
      "Wallet shows normal behavior patterns",
      "No immediate concerns identified",
      "Continue standard monitoring"
    ],
    "compliance_status": "Compliant",
    "confidence_level": "High",
    "report_hash": "0xabc123..."
  }
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
| `completed` | Payment confirmed |
| `failed` | Payment failed |
| `unknown` | Payment status unclear |

**Status Codes:**
- `200 OK` - Status retrieved successfully
- `404 Not Found` - Job ID not found

**Example:**
```bash
curl "http://localhost:8000/status?job_id=550e8400-e29b-41d4-a716-446655440000"
```

---

### cURL Examples

**Complete Workflow:**

```bash
# 1. Check health
curl http://localhost:8000/health

# 2. Check availability
curl http://localhost:8000/availability

# 3. Get input schema
curl http://localhost:8000/input_schema

# 4. Start job
JOB_RESPONSE=$(curl -X POST http://localhost:8000/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "curl_test_001",
    "input_data": {
      "wallet_address": "addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj83ws8lhrn648jjxtwq2ytjqp"
    }
  }')


# 5. Check status (repeat until completed)
curl "http://localhost:8000/status?job_id=$JOB_ID"
```

---

## 🔗 Related Documentation

- [Quick Start Guide](QUICK_START.md) - Get started quickly
- [How It Works](HOW_IT_WORKS.md) - Understand the system
- [Integration Guide](INTEGRATION_GUIDE.md) - Integrate with your app
- [Usage Examples](USAGE_EXAMPLES.md) - Real-world examples

---

## 📞 Support

Need help with the API?

- 📖 Check the [FAQ](FAQ.md)
- 🐛 [Report API issues](https://github.com/your-repo/issues)
- 💬 Join our developer chat
- 📧 Email: api-support@risklens.ai

---

**Last Updated:** 29/11/2025  
**API Version:** 1.0.0  
**Team:** X07

---

**Built with ❤️ by Team X07 for the Cardano Hackathon**


