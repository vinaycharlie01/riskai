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

## 📊 Data Models

### StartJobRequest

```typescript
interface StartJobRequest {
  identifier_from_purchaser: string;  // Unique client identifier
  input_data: {
    wallet_address: string;           // Blockchain wallet address
  };
}
```

### JobResponse

```typescript
interface JobResponse {
  status: string;                     // "success" or "error"
  job_id: string;                     // UUID for the job
  blockchainIdentifier: string;       // Payment identifier
  submitResultTime: string;           // ISO 8601 timestamp
  unlockTime: string;                 // ISO 8601 timestamp
  externalDisputeUnlockTime: string;  // ISO 8601 timestamp
  agentIdentifier: string;            // Agent ID
  sellerVKey: string;                 // Seller verification key
  identifierFromPurchaser: string;    // Echo of input
  amounts: Amount[];                  // Payment amounts
  input_hash: string;                 // Hash of input data
  payByTime: string;                  // ISO 8601 timestamp
}
```

### Amount

```typescript
interface Amount {
  amount: string;   // Amount in smallest unit (e.g., lovelace)
  unit: string;     // Currency unit (e.g., "lovelace", "ADA")
}
```

### StatusResponse

```typescript
interface StatusResponse {
  job_id: string;           // Job identifier
  status: JobStatus;        // Current job status
  payment_status: string;   // Payment status
  result?: RiskReport;      // Analysis result (if completed)
}

type JobStatus = "awaiting_payment" | "running" | "completed" | "failed";
```

### RiskReport

```typescript
interface RiskReport {
  wallet_address: string;
  analysis_timestamp: string;
  risk_score: number;              // 0-100
  risk_category: RiskCategory;
  trust_score: number;             // 0-100
  executive_summary: string;
  transaction_summary: TransactionSummary;
  risk_factors: RiskFactor[];
  suspicious_activities: SuspiciousActivity[];
  recommendations: string[];
  compliance_status: ComplianceStatus;
  confidence_level: ConfidenceLevel;
  report_hash: string;
}

type RiskCategory = "Low Risk" | "Medium Risk" | "High Risk" | "Critical Risk";
type ComplianceStatus = "Compliant" | "Non-Compliant" | "Requires Review";
type ConfidenceLevel = "High" | "Medium" | "Low";
```

### TransactionSummary

```typescript
interface TransactionSummary {
  total_transactions: number;
  total_volume: string;
  active_period: string;
  counterparties: number;
}
```

### RiskFactor

```typescript
interface RiskFactor {
  factor: string;
  severity: Severity;
  description: string;
  impact: string;
}

type Severity = "Low" | "Medium" | "High" | "Critical";
```

### SuspiciousActivity

```typescript
interface SuspiciousActivity {
  activity: string;
  severity: Severity;
  evidence: string;
}
```

---

## ⚠️ Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| `400 Bad Request` | Invalid input | Missing fields, invalid wallet address |
| `404 Not Found` | Resource not found | Invalid job_id |
| `500 Internal Server Error` | Server error | Configuration issues, service unavailable |

### Error Examples

**Missing Required Field:**
```json
{
  "detail": "Input_data or identifier_from_purchaser is missing, invalid, or does not adhere to the schema."
}
```

**Job Not Found:**
```json
{
  "detail": "Job not found"
}
```

**Agent Not Configured:**
```json
{
  "detail": "Agent identifier not configured"
}
```

---

## 🚦 Rate Limits

**Current Status:** No rate limiting implemented

**Recommended Limits (for production):**
- `/start_job`: 10 requests per minute per IP
- `/status`: 60 requests per minute per IP
- Other endpoints: 100 requests per minute per IP

---

## 💡 Usage Examples

### Python Example

```python
import requests
import time

# Base URL
BASE_URL = "http://localhost:8000"

# 1. Start a job
response = requests.post(
    f"{BASE_URL}/start_job",
    json={
        "identifier_from_purchaser": "python_client_001",
        "input_data": {
            "wallet_address": "addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj83ws8lhrn648jjxtwq2ytjqp"
        }
    }
)

job_data = response.json()
job_id = job_data["job_id"]
print(f"Job created: {job_id}")

# 2. Wait for payment (in real scenario, user completes payment)
print("Complete payment on Masumi Network...")
time.sleep(5)

# 3. Poll for results
while True:
    status_response = requests.get(
        f"{BASE_URL}/status",
        params={"job_id": job_id}
    )
    
    status_data = status_response.json()
    print(f"Status: {status_data['status']}")
    
    if status_data["status"] == "completed":
        print("Analysis complete!")
        print(f"Risk Score: {status_data['result']['risk_score']}")
        print(f"Risk Category: {status_data['result']['risk_category']}")
        break
    elif status_data["status"] == "failed":
        print("Analysis failed!")
        break
    
    time.sleep(5)
```

### JavaScript Example

```javascript
const BASE_URL = 'http://localhost:8000';

async function analyzeWallet(walletAddress) {
  // 1. Start job
  const startResponse = await fetch(`${BASE_URL}/start_job`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      identifier_from_purchaser: 'js_client_001',
      input_data: {
        wallet_address: walletAddress
      }
    })
  });
  
  const jobData = await startResponse.json();
  const jobId = jobData.job_id;
  console.log(`Job created: ${jobId}`);
  
  // 2. Poll for results
  while (true) {
    const statusResponse = await fetch(
      `${BASE_URL}/status?job_id=${jobId}`
    );
    
    const statusData = await statusResponse.json();
    console.log(`Status: ${statusData.status}`);
    
    if (statusData.status === 'completed') {
      console.log('Analysis complete!');
      console.log(`Risk Score: ${statusData.result.risk_score}`);
      console.log(`Risk Category: ${statusData.result.risk_category}`);
      return statusData.result;
    } else if (statusData.status === 'failed') {
      throw new Error('Analysis failed');
    }
    
    await new Promise(resolve => setTimeout(resolve, 5000));
  }
}

// Usage
analyzeWallet('addr_test1...')
  .then(result => console.log('Result:', result))
  .catch(error => console.error('Error:', error));
```

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

# Extract job_id (requires jq)
JOB_ID=$(echo $JOB_RESPONSE | jq -r '.job_id')
echo "Job ID: $JOB_ID"

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

**Built with ❤️ by Team X07 for the Masumi Hackathon**

// Made with Bob
