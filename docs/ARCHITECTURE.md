# 🏗️ RiskLens AI - Architecture Overview

Complete system architecture documentation for RiskLens AI blockchain compliance and risk scoring agent.

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Design Patterns](#design-patterns)
7. [Scalability](#scalability)
8. [Security Architecture](#security-architecture)

---

## 🎯 System Overview

RiskLens AI is a **decentralized AI agent** that analyzes blockchain wallet transactions to detect risks, suspicious behavior, and compliance issues. It operates on the **Masumi Network** and uses **multi-agent AI architecture** powered by CrewAI.

### Key Characteristics

- **Decentralized:** Runs on Masumi Agent Network
- **AI-Powered:** Uses GPT-4 via CrewAI framework
- **Pay-Per-Use:** Masumi payment integration
- **On-Chain:** Results stored on Cardano blockchain
- **Async:** Non-blocking operations throughout
- **Modular:** Clean separation of concerns

---

## 🏛️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  • Web Applications    • Mobile Apps    • CLI Tools             │
│  • Exchanges          • DeFi Platforms  • Wallet Providers      │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│                        (FastAPI)                                 │
├─────────────────────────────────────────────────────────────────┤
│  Endpoints:                                                      │
│  • POST /start_job      • GET /status                          │
│  • GET /availability    • GET /input_schema                    │
│  • GET /health                                                  │
└────────────┬────────────────────────────┬───────────────────────┘
             │                            │
             ▼                            ▼
┌────────────────────────┐    ┌──────────────────────────┐
│   PAYMENT LAYER        │    │   ORCHESTRATION LAYER    │
│   (Masumi Network)     │    │   (Job Management)       │
├────────────────────────┤    ├──────────────────────────┤
│ • Payment Requests     │    │ • Job Queue              │
│ • Status Monitoring    │    │ • State Management       │
│ • Payment Completion   │    │ • Callback Handling      │
│ • On-Chain Recording   │    │ • Error Recovery         │
└────────────┬───────────┘    └──────────┬───────────────┘
             │                           │
             └───────────┬───────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI PROCESSING LAYER                           │
│                      (CrewAI Framework)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Agent 1:        │  │  Agent 2:        │  │  Agent 3:    │ │
│  │  Transaction     │→ │  Risk            │→ │  Compliance  │ │
│  │  Analyzer        │  │  Scorer          │  │  Reporter    │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│           │                     │                     │         │
│           └─────────────────────┴─────────────────────┘         │
│                              │                                  │
└──────────────────────────────┼──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │  Blockchain      │         │  AI Tools        │            │
│  │  Analyzer        │         │  (Custom Tools)  │            │
│  └────────┬─────────┘         └──────────────────┘            │
│           │                                                     │
└───────────┼─────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  Blockfrost  │  │  OpenAI      │  │  Cardano Blockchain  │ │
│  │  API         │  │  GPT-4       │  │  (Preprod/Mainnet)   │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Component Details

### 1. API Gateway Layer

**File:** [`main.py`](../main.py)

**Responsibilities:**
- HTTP request handling
- Input validation (Pydantic)
- Response formatting
- Error handling
- Logging

**Key Features:**
- FastAPI framework
- Async/await support
- OpenAPI documentation
- CORS support (configurable)

**Endpoints:**
```python
POST   /start_job      # Submit analysis request
GET    /status         # Check job status
GET    /availability   # Check agent availability
GET    /input_schema   # Get input format
GET    /health         # Health check
```

---

### 2. Payment Layer

**Integration:** Masumi Network SDK

**Responsibilities:**
- Payment request creation
- Payment status monitoring
- Payment completion
- On-chain result storage

**Flow:**
```
1. Create payment request
2. Return payment details to client
3. Monitor payment status (async)
4. Trigger analysis on payment confirmation
5. Store result hash on-chain
```

**Key Classes:**
```python
from masumi.config import Config
from masumi.payment import Payment, Amount

config = Config(
    payment_service_url=PAYMENT_SERVICE_URL,
    payment_api_key=PAYMENT_API_KEY
)

payment = Payment(
    agent_identifier=agent_identifier,
    config=config,
    identifier_from_purchaser=identifier,
    input_data=input_data,
    network=NETWORK
)
```

---

### 3. Orchestration Layer

**File:** [`main.py`](../main.py) (Job Management)

**Responsibilities:**
- Job lifecycle management
- State tracking
- Callback coordination
- Error recovery

**Job States:**
```
awaiting_payment → running → completed
                          ↘ failed
```

**Data Structure:**
```python
jobs = {
    "job_id": {
        "status": "awaiting_payment",
        "payment_status": "pending",
        "blockchain_identifier": "payment_id",
        "input_data": {...},
        "result": None,
        "identifier_from_purchaser": "user_id"
    }
}
```

---

### 4. AI Processing Layer

**File:** [`risk_analysis_crew.py`](../risk_analysis_crew.py)

**Framework:** CrewAI

**Architecture:** Multi-Agent System

#### Agent 1: Transaction Analyzer

**Role:** Blockchain Transaction Analyzer

**Capabilities:**
- Pattern recognition
- Anomaly detection
- Mixer usage identification
- Scam address detection
- Rapid transfer analysis

**Tools:**
- BlockchainAnalysisTool

**Output:**
- Transaction pattern summary
- Suspicious activities list
- Risk indicators
- Behavioral patterns

#### Agent 2: Risk Scorer

**Role:** Risk Assessment Specialist

**Capabilities:**
- Risk score calculation (0-100)
- Category assignment
- Factor weighting
- Confidence assessment

**Input:**
- Transaction analysis results

**Output:**
- Risk score (0-100)
- Risk category (Low/Medium/High/Critical)
- Risk factor breakdown
- Confidence level

#### Agent 3: Compliance Reporter

**Role:** Compliance Report Specialist

**Capabilities:**
- Report generation
- Summary creation
- Recommendation formulation
- Compliance status determination

**Input:**
- Transaction analysis
- Risk assessment

**Output:**
- Complete JSON report
- Executive summary
- Recommendations
- Compliance status

---

### 5. Data Access Layer

#### Blockchain Analyzer

**File:** [`blockchain_analyzer.py`](../blockchain_analyzer.py)

**Responsibilities:**
- Fetch blockchain data
- Analyze transaction patterns
- Calculate risk indicators
- Generate preliminary scores

**Key Methods:**
```python
class BlockchainAnalyzer:
    def get_address_info(address: str) -> Dict
    def get_transactions(address: str, count: int) -> List[Dict]
    def analyze_transaction_patterns(transactions: List) -> Dict
    def calculate_risk_score(analysis: Dict) -> int
```

**Data Sources:**
- Blockfrost API (primary)
- Mock data (fallback for testing)

#### Blockchain Tools

**File:** [`blockchain_tools.py`](../blockchain_tools.py)

**Purpose:** CrewAI tool integration

**Implementation:**
```python
class BlockchainAnalysisTool(BaseTool):
    name: str = "Blockchain Transaction Analyzer"
    description: str = "Analyzes blockchain wallet transactions..."
    args_schema: Type[BaseModel] = BlockchainAnalysisInput
    
    def _run(self, wallet_address: str) -> str:
        data = get_blockchain_data(wallet_address)
        return json.dumps(result, indent=2)
```

---

### 6. External Services Layer

#### Blockfrost API

**Purpose:** Cardano blockchain data access

**Endpoints Used:**
- `/addresses/{address}` - Address info
- `/addresses/{address}/transactions` - Transaction history
- `/transactions/{hash}` - Transaction details

**Configuration:**
```python
api = BlockFrostApi(
    project_id=BLOCKFROST_PROJECT_ID,
    base_url=f"https://cardano-{network}.blockfrost.io/api/v0"
)
```

#### OpenAI GPT-4

**Purpose:** AI agent intelligence

**Usage:**
- Natural language understanding
- Pattern recognition
- Report generation
- Decision making

**Configuration:**
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

#### Cardano Blockchain

**Purpose:** On-chain result storage

**Network:** Preprod (testing) / Mainnet (production)

**Stored Data:**
- Payment records
- Result hashes
- Timestamps
- Agent identifiers

---

## 🔄 Data Flow

### Complete Request Flow

```
1. CLIENT REQUEST
   ↓
   POST /start_job
   {
     "identifier_from_purchaser": "user_001",
     "input_data": {
       "wallet_address": "addr_test1..."
     }
   }

2. API GATEWAY
   ↓
   • Validate input (Pydantic)
   • Generate job_id (UUID)
   • Create payment request (Masumi)
   ↓
   Return payment details

3. PAYMENT MONITORING
   ↓
   • Monitor payment status (async)
   • Wait for payment confirmation
   ↓
   Payment confirmed!

4. AI PROCESSING
   ↓
   • Fetch blockchain data (Blockfrost)
   • Agent 1: Analyze transactions
   • Agent 2: Calculate risk score
   • Agent 3: Generate report
   ↓
   Analysis complete

5. RESULT STORAGE
   ↓
   • Store result in job store
   • Complete payment on Masumi
   • Store hash on Cardano blockchain
   ↓
   Job status: completed

6. CLIENT RETRIEVAL
   ↓
   GET /status?job_id=xxx
   ↓
   Return complete report
```

### Data Transformation Pipeline

```
Raw Blockchain Data
    ↓
[Blockfrost API]
    ↓
Transaction List
    ↓
[Blockchain Analyzer]
    ↓
Pattern Analysis
    ↓
[Transaction Analyzer Agent]
    ↓
Risk Indicators
    ↓
[Risk Scorer Agent]
    ↓
Risk Score + Category
    ↓
[Compliance Reporter Agent]
    ↓
Complete JSON Report
    ↓
[Result Storage]
    ↓
Client Response
```

---

## 🛠️ Technology Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### AI & ML
- **CrewAI** - Multi-agent orchestration
- **OpenAI GPT-4** - Language model
- **LangChain** - AI framework (via CrewAI)

### Blockchain
- **Blockfrost** - Cardano API
- **Masumi SDK** - Payment integration
- **Cardano** - Blockchain network

### Data & Storage
- **Python Dict** - In-memory storage (dev)
- **Redis** - Recommended for production
- **PostgreSQL** - Alternative for production

### DevOps
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **GitHub Actions** - CI/CD (recommended)

### Monitoring & Logging
- **Python Logging** - Built-in logging
- **Rotating File Handler** - Log management
- **Prometheus** - Metrics (recommended)

---

## 🎨 Design Patterns

### 1. Multi-Agent Pattern

**Pattern:** Specialized agents working together

**Implementation:**
```python
crew = Crew(
    agents=[transaction_analyzer, risk_scorer, compliance_reporter],
    tasks=[analyze_task, score_task, report_task]
)
```

**Benefits:**
- Clear separation of concerns
- Specialized expertise
- Parallel processing potential
- Easy to extend

### 2. Async/Await Pattern

**Pattern:** Non-blocking I/O operations

**Implementation:**
```python
async def start_job(data: StartJobRequest):
    payment_request = await payment.create_payment_request()
    await payment.start_status_monitoring(callback)
```

**Benefits:**
- Better performance
- Handles concurrent requests
- Non-blocking operations

### 3. Callback Pattern

**Pattern:** Event-driven processing

**Implementation:**
```python
async def payment_callback(blockchain_identifier: str):
    await handle_payment_status(job_id, blockchain_identifier)

await payment.start_status_monitoring(payment_callback)
```

**Benefits:**
- Decoupled components
- Event-driven architecture
- Flexible workflow

### 4. Factory Pattern

**Pattern:** Object creation abstraction

**Implementation:**
```python
class RiskAnalysisCrew:
    def create_crew(self):
        # Create agents
        # Create tasks
        # Return configured crew
```

**Benefits:**
- Centralized configuration
- Easy to modify
- Testable

### 5. Strategy Pattern

**Pattern:** Interchangeable algorithms

**Implementation:**
```python
# Different risk scoring strategies
def calculate_risk_score(analysis: Dict) -> int:
    # Strategy can be swapped
```

**Benefits:**
- Flexible algorithms
- Easy to test
- Maintainable

---

## 📈 Scalability

### Current Limitations

**In-Memory Storage:**
- Limited to single instance
- Data lost on restart
- No horizontal scaling

**Synchronous AI Processing:**
- Blocks during analysis
- Limited concurrency

### Scaling Strategies

#### Horizontal Scaling

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ API     │  │ API     │  │ API     │
│ Instance│  │ Instance│  │ Instance│
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┴────────────┘
                  │
          ┌───────▼────────┐
          │  Load Balancer │
          └───────┬────────┘
                  │
          ┌───────▼────────┐
          │  Redis Cluster │
          └────────────────┘
```

#### Vertical Scaling

- Increase CPU for AI processing
- More memory for caching
- Faster storage for logs

#### Microservices Architecture

```
┌──────────────┐
│  API Gateway │
└──────┬───────┘
       │
   ┌───┴────┬────────┬──────────┐
   │        │        │          │
┌──▼──┐ ┌──▼──┐ ┌───▼───┐ ┌───▼────┐
│Auth │ │Job  │ │AI     │ │Payment │
│Svc  │ │Mgmt │ │Engine │ │Service │
└─────┘ └─────┘ └───────┘ └────────┘
```

### Performance Optimization

**Caching:**
```python
@lru_cache(maxsize=100)
def get_cached_blockchain_data(wallet_address: str):
    return get_blockchain_data(wallet_address)
```

**Background Tasks:**
```python
@app.post("/start_job")
async def start_job(data: StartJobRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(execute_crew_task, job_id, input_data)
```

**Connection Pooling:**
```python
# Redis connection pool
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50
)
```

---

## 🔒 Security Architecture

### Authentication & Authorization

**Current:** Payment-based access control

**Recommended:**
- API key authentication
- JWT tokens
- Role-based access control (RBAC)

### Data Security

**In Transit:**
- HTTPS/TLS encryption
- Secure WebSocket connections

**At Rest:**
- Encrypted storage (recommended)
- Secure key management

### Input Validation

```python
class StartJobRequest(BaseModel):
    identifier_from_purchaser: str
    input_data: dict[str, str]
    
    @field_validator('input_data')
    def validate_wallet_address(cls, v):
        # Validation logic
        return v
```

### Rate Limiting

**Recommended Implementation:**
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/start_job")
@limiter.limit("10/minute")
async def start_job(...):
    ...
```

### Security Best Practices

✅ **Implemented:**
- Environment variables for secrets
- Input validation
- Error handling
- Logging

⚠️ **Recommended:**
- Rate limiting
- API authentication
- Request signing
- Audit logging
- Security headers

---

## 📊 Monitoring & Observability

### Logging

**Current Implementation:**
```python
logger.info("Starting RiskLens AI analysis")
logger.error("Error in start_job", exc_info=True)
```

**Log Levels:**
- INFO: Normal operations
- WARNING: Potential issues
- ERROR: Errors with stack traces

### Metrics (Recommended)

**Key Metrics:**
- Request rate
- Response time
- Error rate
- Job completion rate
- Payment success rate
- AI processing time

**Implementation:**
```python
from prometheus_client import Counter, Histogram

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')
```

### Health Checks

**Current:**
```python
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Enhanced:**
```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "uptime": get_uptime(),
        "dependencies": {
            "openai": check_openai(),
            "blockfrost": check_blockfrost(),
            "masumi": check_masumi()
        }
    }
```

---

## 🔗 Related Documentation

- [Quick Start Guide](QUICK_START.md)
- [API Reference](API_REFERENCE.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Code Review](CODE_REVIEW.md)

---

**Last Updated:** 29/11/2025  
**Version:** 1.0.0  
**Team:** X07

---

**Built with ❤️ by Team X07 for the Masumi Hackathon**

// Made with Bob
