# 🏗️ RiskLens AI - System Architecture

**Version:** 1.0.0  
**Last Updated:** December 7, 2025  
**Status:** Production Ready

---

## 📋 Table of Contents

1. [Executive Summary](#-executive-summary)
2. [System Overview](#-system-overview)
3. [Architectural Principles](#-architectural-principles)
4. [High-Level Architecture](#️-high-level-architecture)
5. [Component Architecture](#-component-architecture)
6. [Data Architecture](#-data-architecture)
7. [Integration Architecture](#-integration-architecture)
8. [Deployment Architecture](#-deployment-architecture)
9. [Security Architecture](#-security-architecture)
10. [Scalability & Performance](#-scalability--performance)
11. [Design Decisions & Trade-offs](#-design-decisions--trade-offs)
12. [Future Considerations](#-future-considerations)

---

## 🎯 Executive Summary

RiskLens AI is a **decentralized AI-powered compliance agent** that analyzes blockchain wallet transactions to detect risks, suspicious behavior, and compliance issues. The system operates on the **Masumi Network** using a **multi-agent AI architecture** powered by CrewAI, with real-time blockchain data from Blockfrost API.

### Key Architectural Characteristics

| Characteristic | Implementation |
|---------------|----------------|
| **Architecture Style** | Microservices-ready, Event-driven |
| **Deployment Model** | Cloud-native (Railway) |
| **Data Storage** | MongoDB (persistent), In-memory (transient) |
| **AI Framework** | CrewAI (multi-agent orchestration) |
| **Blockchain Integration** | Blockfrost API (Cardano) |
| **Payment Protocol** | Masumi Network (MIP-003 compliant) |
| **API Style** | RESTful, Async/Await |
| **Scalability** | Horizontal (stateless API) + Vertical (AI processing) |

---

## 🌐 System Overview

### Purpose & Scope

RiskLens AI provides **automated blockchain wallet risk assessment** for:
- **Crypto Exchanges** - KYC/AML compliance
- **DeFi Platforms** - Liquidity pool protection
- **Regulators** - Automated monitoring
- **Individual Users** - Transaction safety verification

### Core Capabilities

```mermaid
    A[Wallet Address] --> B[Blockchain Data Fetch]
    B --> C[AI Analysis]
    C --> D[Risk Scoring]
    D --> E[Compliance Report]
    E --> F[On-Chain Storage]
```

1. **Real-time Data Acquisition** - Fetch transaction history from Cardano blockchain
2. **Multi-Agent AI Analysis** - Three specialized agents analyze patterns
3. **Risk Quantification** - Calculate 0-100 risk scores with categorization
4. **Compliance Reporting** - Generate detailed, actionable reports
5. **On-Chain Verification** - Store report hashes on Cardano blockchain

---

## 🎨 Architectural Principles

### 1. **Separation of Concerns**
Each component has a single, well-defined responsibility:
- API Gateway handles HTTP/REST
- Payment Layer manages Masumi integration
- AI Layer performs analysis
- Data Layer handles persistence

### 2. **Asynchronous by Default**
All I/O operations use async/await:
- Non-blocking API endpoints
- Concurrent payment monitoring
- Async database operations
- Parallel external API calls

### 3. **Fail-Safe Design**
Graceful degradation when services unavailable:
- Mock data fallback (Blockfrost unavailable)
- Retry logic for transient failures
- Comprehensive error logging
- Health check endpoints

### 4. **Cloud-Native**
Designed for cloud deployment:
- Stateless API (horizontal scaling)
- External state management (MongoDB)
- Environment-based configuration
- Container-ready

### 5. **Standards Compliance**
Adheres to industry standards:
- MIP-003 (Masumi Integration Protocol)
- RESTful API design
- OpenAPI/Swagger documentation
- JSON data interchange

---

## 🏛️ High-Level Architecture

### System Context Diagram


```
┌─────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL ACTORS                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Exchange │  │   DeFi   │  │   User   │  │    Sokosumi      │  │
│  │   KYC    │  │ Platform │  │  Wallet  │  │    Dashboard     │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬─────────┘  │
│       │             │              │                  │             │
└───────┼─────────────┼──────────────┼──────────────────┼─────────────┘
        │             │              │                  │
        └─────────────┴──────────────┴──────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │         RISKLENS AI SYSTEM                  │
        │         (Railway Deployment)                │
        ├─────────────────────────────────────────────┤
        │                                             │
        │  ┌────────────────────────────────────┐   │
        │  │      API GATEWAY LAYER             │   │
        │  │      (FastAPI + Uvicorn)           │   │
        │  └──────────────┬─────────────────────┘   │
        │                 │                          │
        │  ┌──────────────┴─────────────────────┐   │
        │  │    ORCHESTRATION & PAYMENT         │   │
        │  │    (Job Management + Masumi)       │   │
        │  └──────────────┬─────────────────────┘   │
        │                 │                          │
        │  ┌──────────────┴─────────────────────┐   │
        │  │      AI PROCESSING LAYER           │   │
        │  │      (CrewAI Multi-Agent)          │   │
        │  └──────────────┬─────────────────────┘   │
        │                 │                          │
        │  ┌──────────────┴─────────────────────┐   │
        │  │      DATA ACCESS LAYER             │   │
        │  │   (MongoDB + Blockfrost API)       │   │
        │  └────────────────────────────────────┘   │
        │                                             │
        └─────────────────┬───────────────────────────┘
                          │
        ┌─────────────────┴───────────────────────────┐
        │         EXTERNAL SERVICES                    │
        ├──────────────────────────────────────────────┤
        │                                              │
        │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
        │  │Blockfrost│  │  OpenAI  │  │  Cardano │ │
        │  │   API    │  │  GPT-4   │  │Blockchain│ │
        │  └──────────┘  └──────────┘  └──────────┘ │
        │                                              │
        └──────────────────────────────────────────────┘
```

### Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                      │
│  • REST API Endpoints (MIP-003 Compliant)              │
│  • Request Validation (Pydantic)                        │
│  • Response Formatting (String for Sokosumi)           │
│  • OpenAPI Documentation                                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                   │
│  • Job Orchestration & State Management                │
│  • Payment Processing (Masumi SDK)                     │
│  • AI Agent Coordination (CrewAI)                      │
│  • Result Formatting & Validation                      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                   DATA ACCESS LAYER                      │
│  • MongoDB Operations (Motor Async)                    │
│  • Blockchain Data Fetching (Blockfrost)               │
│  • External API Integration                            │
│  • Caching & Optimization                              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                   │
│  • Logging (File + Console/Stdout)                     │
│  • Configuration Management (.env)                      │
│  • Health Monitoring                                    │
│  • Error Handling & Recovery                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Component Architecture

### 1. API Gateway Layer

**Files:**
- [`main.py`](../main.py) - Application entry point
- [`api/routes/job_routes.py`](../api/routes/job_routes.py) - Job management endpoints
- [`api/routes/agent_routes.py`](../api/routes/agent_routes.py) - Agent info endpoints
- [`api/models.py`](../api/models.py) - Pydantic request/response models

**Responsibilities:**
- HTTP request/response handling
- Input validation using Pydantic models
- Endpoint routing (6 MIP-003 compliant endpoints)
- Error handling and logging
- Application lifecycle management

**Key Design Patterns:**
- **Lifespan Context Manager** - Modern FastAPI pattern for startup/shutdown
- **Dependency Injection** - MongoDB connection management
- **Async/Await** - Non-blocking I/O operations

**Implementation Details:**

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize resources
    await mongo_store.connect()
    logger.info(" Application started")
    yield
    # Shutdown: Cleanup resources
    await mongo_store.disconnect()
    logger.info("Application shutdown complete")

app = FastAPI(
    title="RiskLens AI",
    version="1.0.0",
    lifespan=lifespan  # Modern pattern (replaces @app.on_event)
)
```

**Endpoints Architecture:**

| Endpoint | Method | Purpose | MIP-003 |
|----------|--------|---------|---------|
| `/` | GET | Root/Info |  |
| `/start_job` | POST | Initiate analysis |  Required |
| `/status` | GET | Check job status |  Required |
| `/availability` | GET | Agent availability |  Required |
| `/input_schema` | GET | Input format |  Required |
| `/health` | GET | Health check |  |

---

### 2. Payment & Orchestration Layer

**Files:**
- [`services/payment/masumi_service.py`](../services/payment/masumi_service.py) - Payment service
- [`core/crew.py`](../core/crew.py) - CrewAI orchestration

**Integration:** Masumi Network SDK

**Architecture Pattern:** Event-Driven with Callbacks

**Components:**

```
┌─────────────────────────────────────────────────────┐
│           PAYMENT ORCHESTRATION                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  Payment Request Creation                    │  │
│  │  • Generate unique job ID                    │  │
│  │  • Create Masumi payment request             │  │
│  │  • Store job in MongoDB (awaiting_payment)   │  │
│  └──────────────┬───────────────────────────────┘  │
│                 │                                   │
│  ┌──────────────▼───────────────────────────────┐  │
│  │  Payment Status Monitoring (Async)           │  │
│  │  • Poll Masumi API for payment status        │  │
│  │  • Trigger callback on payment confirmation  │  │
│  │  • Handle payment failures                   │  │
│  └──────────────┬───────────────────────────────┘  │
│                 │                                   │
│  ┌──────────────▼───────────────────────────────┐  │
│  │  Job Execution Trigger                       │  │
│  │  • Update job status to 'running'            │  │
│  │  • Execute AI analysis                       │  │
│  │  • Format and submit result                  │  │
│  └──────────────┬───────────────────────────────┘  │
│                 │                                   │
│  ┌──────────────▼───────────────────────────────┐  │
│  │  Result Submission                           │  │
│  │  • Format result as string (Sokosumi)        │  │
│  │  • Submit to Masumi (complete_payment)       │  │
│  │  • Store hash on Cardano blockchain          │  │
│  │  • Update job status to 'completed'          │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**State Machine:**

```
┌─────────────────┐
│ awaiting_payment│
└────────┬────────┘
         │ Payment Confirmed
         ▼
┌─────────────────┐
│    running      │
└────────┬────────┘
         │ Analysis Complete
         ▼
┌─────────────────┐     ┌─────────────────┐
│   completed     │     │     failed      │
└─────────────────┘     └─────────────────┘
```

**Job Data Structure:**

```python
{
    "job_id": "uuid",
    "status": "awaiting_payment|running|completed|failed",
    "payment_status": "pending|paid|result_submitted",
    "blockchain_identifier": "payment_id",
    "input_data": {"wallet_address": "addr_test1..."},
    "result": "formatted_string_report",
    "result_hash": "0xabc123...",
    "identifier_from_purchaser": "user_id",
    "error": "error_message (if failed)"
}
```

---

### 3. AI Processing Layer

**Files:**
- [`core/crew.py`](../core/crew.py) - CrewAI orchestration
- [`agents/transaction_analyzer/agent.py`](../agents/transaction_analyzer/agent.py) - Transaction analyzer
- [`agents/risk_scorer/agent.py`](../agents/risk_scorer/agent.py) - Risk scorer
- [`agents/compliance_reporter/agent.py`](../agents/compliance_reporter/agent.py) - Compliance reporter

**Framework:** CrewAI (Multi-Agent Orchestration)

**Architecture Pattern:** Pipeline with Specialized Agents

```
┌─────────────────────────────────────────────────────────────┐
│              AI PROCESSING PIPELINE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  INPUT: wallet_address                                      │
│     │                                                        │
│     ▼                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AGENT 1: Transaction Analyzer                       │  │
│  │  ─────────────────────────────────────────────────   │  │
│  │  Role: Blockchain Transaction Analyzer               │  │
│  │  Tools: BlockchainAnalysisTool                       │  │
│  │                                                       │  │
│  │  Tasks:                                              │  │
│  │  • Fetch transaction data via Blockfrost            │  │
│  │  • Identify patterns (frequency, amounts, timing)   │  │
│  │  • Detect anomalies (mixers, rapid transfers)       │  │
│  │  • Flag suspicious activities                       │  │
│  │                                                       │  │
│  │  Output: Transaction analysis report                │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│                     ▼                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AGENT 2: Risk Scorer                                │  │
│  │  ─────────────────────────────────────────────────   │  │
│  │  Role: Risk Assessment Specialist                    │  │
│  │  Tools: None (uses Agent 1 output)                   │  │
│  │                                                       │  │
│  │  Tasks:                                              │  │
│  │  • Analyze transaction patterns                     │  │
│  │  • Calculate risk score (0-100)                     │  │
│  │  • Assign risk category (Low/Med/High/Critical)     │  │
│  │  • Determine confidence level                       │  │
│  │  • Explain risk factors                             │  │
│  │                                                       │  │
│  │  Scoring Logic:                                      │  │
│  │  • Base: 20 points                                   │  │
│  │  • High frequency: +15                               │  │
│  │  • Large transactions: +25                           │  │
│  │  • Unusual fees: +15                                 │  │
│  │  • Critical indicators: +40                          │  │
│  │                                                       │  │
│  │  Output: Risk assessment with score & breakdown     │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│                     ▼                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  AGENT 3: Compliance Reporter                        │  │
│  │  ─────────────────────────────────────────────────   │  │
│  │  Role: Compliance Report Specialist                  │  │
│  │  Tools: None (uses Agent 1 & 2 outputs)              │  │
│  │                                                       │  │
│  │  Tasks:                                              │  │
│  │  • Generate executive summary                       │  │
│  │  • Create transaction summary                       │  │
│  │  • List risk factors with severity                  │  │
│  │  • Document suspicious activities                   │  │
│  │  • Provide actionable recommendations               │  │
│  │  • Determine compliance status                      │  │
│  │  • Format as structured JSON                        │  │
│  │                                                       │  │
│  │  Output: Complete JSON compliance report            │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                       │
│                     ▼                                       │
│  OUTPUT: Structured JSON report                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Agent Communication:**
- **Sequential Processing** - Each agent builds on previous agent's output
- **Context Sharing** - Agents share analysis context via CrewAI
- **LLM-Powered** - All agents use OpenAI GPT-4 for intelligence

**Why Multi-Agent?**
1. **Specialization** - Each agent focuses on specific expertise
2. **Modularity** - Easy to add/modify agents independently
3. **Quality** - Multiple perspectives improve accuracy
4. **Explainability** - Clear reasoning chain from analysis to report

---

### 4. Data Access Layer

#### 4.1 Blockchain Data Access

**Files:**
- [`services/blockchain/analyzer.py`](../services/blockchain/analyzer.py) - Blockchain data fetching
- [`services/blockchain/tools.py`](../services/blockchain/tools.py) - CrewAI tools

**Purpose:** Fetch and analyze real blockchain data

**Architecture:**

```
┌─────────────────────────────────────────────────────┐
│         BLOCKCHAIN DATA ACCESS                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  BlockchainAnalyzer Class                  │    │
│  │  ────────────────────────────────────────  │    │
│  │                                            │    │
│  │  Initialization:                           │    │
│  │  • Check BLOCKFROST_PROJECT_ID env var    │    │
│  │  • Initialize Blockfrost API client        │    │
│  │  • Set network (preprod/mainnet)          │    │
│  │  • Fallback to mock data if no API key    │    │
│  │                                            │    │
│  │  Methods:                                  │    │
│  │  ┌──────────────────────────────────────┐ │    │
│  │  │ get_address_info(address)            │ │    │
│  │  │ • Fetch address metadata             │ │    │
│  │  │ • Get stake address                  │ │    │
│  │  │ • Determine address type             │ │    │
│  │  └──────────────────────────────────────┘ │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────────┐ │    │
│  │  │ get_transactions(address, count)     │ │    │
│  │  │ • Fetch up to 100 transactions       │ │    │
│  │  │ • Get tx hash, block, time, amounts  │ │    │
│  │  │ • Calculate fees and sizes           │ │    │
│  │  └──────────────────────────────────────┘ │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────────┐ │    │
│  │  │ analyze_transaction_patterns(txs)    │ │    │
│  │  │ • Calculate total volume             │ │    │
│  │  │ • Detect high frequency (>50 txs)    │ │    │
│  │  │ • Find large transactions (>100k)    │ │    │
│  │  │ • Identify unusual fee patterns      │ │    │
│  │  │ • Calculate time span                │ │    │
│  │  └──────────────────────────────────────┘ │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────────┐ │    │
│  │  │ calculate_risk_score(analysis)       │ │    │
│  │  │ • Base score: 20                     │ │    │
│  │  │ • Add points per risk indicator      │ │    │
│  │  │ • Cap at 100                         │ │    │
│  │  └──────────────────────────────────────┘ │    │
│  │                                            │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  Fallback Strategy:                                 │
│  • Real data: Blockfrost API (when key present)    │
│  • Mock data: Generated test data (no API key)     │
│  • Logging: Clear indication of data source        │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Data Flow:**

```
Wallet Address
     │
     ▼
┌─────────────────┐
│ Blockfrost API  │ ◄─── BLOCKFROST_PROJECT_ID
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Raw Transaction │
│      Data       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Pattern      │
│    Analysis     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Risk Score     │
│  Calculation    │
└─────────────────┘
```

#### 4.2 Persistent Storage

**File:** [`services/storage/mongo_store.py`](../services/storage/mongo_store.py)

**Purpose:** Persistent job state management

**Architecture:**

```
┌─────────────────────────────────────────────────────┐
│            MONGODB STORAGE LAYER                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Technology: Motor (Async MongoDB Driver)           │
│  Database: risklens_ai (configurable via env)      │
│  Collection: jobs                                    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  MongoStore Class (Singleton Pattern)      │    │
│  │  ────────────────────────────────────────  │    │
│  │                                            │    │
│  │  Lifecycle:                                │    │
│  │  ┌──────────────────────────────────────┐ │    │
│  │  │ connect()                            │ │    │
│  │  │ • Initialize AsyncIOMotorClient      │ │    │
│  │  │ • Create indexes (job_id, bc_id)     │ │    │
│  │  │ • Handle existing index errors       │ │    │
│  │  └──────────────────────────────────────┘ │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────────┐ │    │
│  │  │ disconnect()                         │ │    │
│  │  │ • Close MongoDB connection           │ │    │
│  │  │ • Cleanup resources                  │ │    │
│  │  └──────────────────────────────────────┘ │    │
│  │                                            │    │
│  │  Operations:                               │    │
│  │  ┌──────────────────────────────────────┐ │    │
│  │  │ set_job(job_id, data)                │ │    │
│  │  │ • Insert new job document            │ │    │
│  │  │ • Upsert if exists                   │ │    │
│  │  └──────────────────────────────────────┘ │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────────┐ │    │
│  │  │ get_job(job_id)                      │ │    │
│  │  │ • Retrieve job by ID                 │ │    │
│  │  │ • Return None if not found           │ │    │
│  │  └──────────────────────────────────────┘ │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────────┐ │    │
│  │  │ update_job(job_id, updates)          │ │    │
│  │  │ • Partial update using $set          │ │    │
│  │  │ • Atomic operation                   │ │    │
│  │  └──────────────────────────────────────┘ │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────────┐ │    │
│  │  │ ping()                               │ │    │
│  │  │ • Health check                       │ │    │
│  │  │ • Verify connection                  │ │    │
│  │  └──────────────────────────────────────┘ │    │
│  │                                            │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  Indexes:                                           │
│  • job_id (unique) - Fast job lookup                │
│  • blockchain_identifier - Payment tracking         │
│                                                      │
│  Benefits:                                          │
│  • Persistence across restarts                      │
│  • Horizontal scaling support                       │
│  • Async operations (non-blocking)                  │
│  • ACID transactions                                │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 📊 Data Architecture

### Data Models

#### 1. Job Model

```python
{
    "_id": ObjectId,  # MongoDB internal ID
    "job_id": "uuid-string",  # Unique job identifier
    "status": "awaiting_payment|running|completed|failed",
    "payment_status": "pending|paid|result_submitted",
    "blockchain_identifier": "payment_id_from_masumi",
    "input_data": {
        "wallet_address": "addr_test1..."
    },
    "result": "formatted_string_report",  # String for Sokosumi
    "result_hash": "0xabc123...",  # On-chain verification
    "identifier_from_purchaser": "user_provided_id",
    "error": "error_message",  # Only if failed
    "created_at": ISODate,
    "updated_at": ISODate
}
```

#### 2. Analysis Result Model

```python
{
    "wallet_address": "addr_test1...",
    "analysis_timestamp": "2025-12-07T10:30:00Z",
    "risk_score": 75,  # 0-100
    "risk_category": "High Risk",
    "trust_score": 25,  # Inverse of risk
    "confidence_level": "High",
    "executive_summary": "text...",
    "transaction_summary": {
        "total_transactions": 150,
        "total_volume": "500 ADA",
        "active_period": "180 days",
        "counterparties": 45
    },
    "risk_factors": [
        {
            "factor": "High Transaction Frequency",
            "severity": "Medium",
            "description": "50+ transactions detected",
            "impact": "Increases risk score by 15 points"
        }
    ],
    "suspicious_activities": [
        "Rapid large transfers",
        "Unusual fee patterns"
    ],
    "recommendations": [
        "Conduct enhanced due diligence",
        "Monitor for additional activity"
    ],
    "compliance_status": "Requires Review",
    "report_hash": "0xabc123..."
}
```

### Data Flow Diagram

```
┌──────────────┐
│   Client     │
│   Request    │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  1. Job Creation                         │
│  • Generate job_id                       │
│  • Store in MongoDB (awaiting_payment)   │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  2. Payment Processing                   │
│  • Monitor Masumi payment status         │
│  • Update MongoDB (payment_status)       │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  3. Blockchain Data Fetch                │
│  • Query Blockfrost API                  │
│  • Get transactions (up to 100)          │
│  • Temporary in-memory storage           │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  4. AI Analysis                          │
│  • CrewAI processes data                 │
│  • Generate JSON report                  │
│  • Temporary in-memory                   │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  5. Result Formatting                    │
│  • Convert JSON to string                │
│  • Format for Sokosumi display           │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  6. Result Storage                       │
│  • Store in MongoDB (result field)       │
│  • Submit to Masumi (on-chain hash)      │
│  • Update status to 'completed'          │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────┐
│   Client     │
│   Response   │
└──────────────┘
```

---

## 🔗 Integration Architecture

### External Service Integration

```
┌─────────────────────────────────────────────────────────┐
│              EXTERNAL INTEGRATIONS                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  1. Blockfrost API (Cardano Blockchain)        │    │
│  │  ────────────────────────────────────────────  │    │
│  │  Purpose: Real blockchain data                 │    │
│  │  Protocol: HTTPS/REST                          │    │
│  │  Authentication: Project ID (API key)          │    │
│  │  Rate Limits: 50 req/sec (paid tier)           │    │
│  │                                                 │    │
│  │  Endpoints Used:                               │    │
│  │  • GET /addresses/{address}                    │    │
│  │  • GET /addresses/{address}/transactions       │    │
│  │  • GET /txs/{hash}/utxos                       │    │
│  │                                                 │    │
│  │  Error Handling:                               │    │
│  │  • Retry on transient failures (3x)            │    │
│  │  • Fallback to mock data                       │    │
│  │  • Comprehensive logging                       │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  2. OpenAI API (GPT-4)                         │    │
│  │  ────────────────────────────────────────────  │    │
│  │  Purpose: AI agent intelligence                │    │
│  │  Protocol: HTTPS/REST                          │    │
│  │  Authentication: API key (Bearer token)        │    │
│  │  Model: gpt-4 (via CrewAI)                     │    │
│  │                                                 │    │
│  │  Usage:                                        │    │
│  │  • Transaction pattern analysis                │    │
│  │  • Risk score calculation                      │    │
│  │  • Report generation                           │    │
│  │                                                 │    │
│  │  Error Handling:                               │    │
│  │  • Retry on rate limits                        │    │
│  │  • Exponential backoff                         │    │
│  │  • Timeout handling (60s)                      │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  3. Masumi Network (Payment Protocol)          │    │
│  │  ────────────────────────────────────────────  │    │
│  │  Purpose: Decentralized payment processing     │    │
│  │  Protocol: MIP-003 (Masumi Integration)        │    │
│  │  Authentication: API key + Agent identifier    │    │
│  │                                                 │    │
│  │  Operations:                                   │    │
│  │  • create_payment_request()                    │    │
│  │  • start_status_monitoring()                   │    │
│  │  • check_payment_status()                      │    │
│  │  • complete_payment(result)                    │    │
│  │                                                 │    │
│  │  Callback Pattern:                             │    │
│  │  • Async payment monitoring                    │    │
│  │  • Event-driven job execution                  │    │
│  │  • On-chain result storage                     │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  4. MongoDB Atlas (Database)                   │    │
│  │  ────────────────────────────────────────────  │    │
│  │  Purpose: Persistent job storage               │    │
│  │  Protocol: MongoDB Wire Protocol               │    │
│  │  Driver: Motor (async)                         │    │
│  │  Connection: mongodb+srv://...                 │    │
│  │                                                 │    │
│  │  Features:                                     │    │
│  │  • Automatic failover                          │    │
│  │  • Connection pooling                          │    │
│  │  • Replica sets                                │    │
│  │  • Encryption at rest                          │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Integration Patterns

1. **Circuit Breaker** - Prevent cascading failures
2. **Retry with Backoff** - Handle transient errors
3. **Timeout Management** - Prevent hanging requests
4. **Fallback Strategies** - Graceful degradation
5. **Health Checks** - Monitor service availability

---

## 🚀 Deployment Architecture

### Railway Cloud Deployment

```
┌─────────────────────────────────────────────────────────┐
│                  RAILWAY PLATFORM                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Application Container                         │    │
│  │  ────────────────────────────────────────────  │    │
│  │                                                 │    │
│  │  Runtime: Python 3.11                          │    │
│  │  Framework: FastAPI + Uvicorn                  │    │
│  │  Port: 8000 (configurable)                     │    │
│  │  Host: 0.0.0.0 (external access)               │    │
│  │                                                 │    │
│  │  Environment Variables:                        │    │
│  │  • OPENAI_API_KEY                              │    │
│  │  • BLOCKFROST_PROJECT_ID                       │    │
│  │  • AGENT_IDENTIFIER                            │    │
│  │  • PAYMENT_API_KEY                             │    │
│  │  • PAYMENT_SERVICE_URL                         │    │
│  │  • SELLER_VKEY                                 │    │
│  │  • MONGO_URL                                   │    │
│  │  • NETWORK (preprod/mainnet)                   │    │
│  │                                                 │    │
│  │  Resources:                                    │    │
│  │  • CPU: 1-2 vCPU                               │    │
│  │  • Memory: 512MB-1GB                           │    │
│  │  • Storage: Ephemeral (logs only)              │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  Automatic Features                            │    │
│  │  ────────────────────────────────────────────  │    │
│  │  • HTTPS/TLS (automatic)                       │    │
│  │  • Custom domain support                       │    │
│  │  • Auto-restart on crash                       │    │
│  │  • Zero-downtime deployments                   │    │
│  │  • Git-based CI/CD                             │    │
│  │  • Environment variable management             │    │
│  │  • Real-time logs (stdout)                     │    │
│  │  • Metrics dashboard                           │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Deployment Process

```
┌──────────────┐
│  Git Push    │
│  to GitHub   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────┐
│  Railway Auto-Deploy             │
│  • Detect changes                │
│  • Build container               │
│  • Run tests (if configured)     │
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│  Health Check                    │
│  • GET /health                   │
│  • Verify MongoDB connection     │
│  • Check external services       │
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│  Traffic Switch                  │
│  • Zero-downtime cutover         │
│  • Old version terminated        │
│  • New version receives traffic  │
└──────────────────────────────────┘
```

### Scalability Configuration

**Current Setup:**
- Single instance (sufficient for MVP)
- Vertical scaling (increase CPU/memory)
- MongoDB handles persistence

**Future Scaling:**
```
┌─────────────────────────────────────────────┐
│  Horizontal Scaling (Multiple Instances)    │
├─────────────────────────────────────────────┤
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Instance 1│  │Instance 2│  │Instance 3│ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
│       │             │              │        │
│       └─────────────┴──────────────┘        │
│                     │                       │
│              ┌──────▼──────┐               │
│              │Railway Load │               │
│              │  Balancer   │               │
│              └──────┬──────┘               │
│                     │                       │
│              ┌──────▼──────┐               │
│              │  MongoDB    │               │
│              │   Atlas     │               │
│              └─────────────┘               │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 🔒 Security Architecture

### Security Layers

```
┌─────────────────────────────────────────────────────────┐
│              SECURITY ARCHITECTURE                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Layer 1: Network Security                              │
│  ┌────────────────────────────────────────────────┐    │
│  │  • HTTPS/TLS encryption (Railway automatic)    │    │
│  │  • DDoS protection (Railway platform)          │    │
│  │  • Rate limiting (recommended)                 │    │
│  │  • IP whitelisting (optional)                  │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Layer 2: Application Security                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  • Input validation (Pydantic models)          │    │
│  │  • SQL injection prevention (MongoDB)          │    │
│  │  • XSS protection (API-only, no HTML)          │    │
│  │  • CORS configuration                          │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Layer 3: Authentication & Authorization                │
│  ┌────────────────────────────────────────────────┐    │
│  │  • Payment-based access (Masumi)               │    │
│  │  • API key authentication (external services)  │    │
│  │  • Environment variable secrets                │    │
│  │  • No hardcoded credentials                    │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Layer 4: Data Security                                 │
│  ┌────────────────────────────────────────────────┐    │
│  │  • Encryption in transit (TLS)                 │    │
│  │  • Encryption at rest (MongoDB Atlas)          │    │
│  │  • No PII storage (public blockchain data)     │    │
│  │  • Secure key management (Railway secrets)     │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Layer 5: Monitoring & Logging                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  • Comprehensive logging (file + console)      │    │
│  │  • Error tracking with stack traces            │    │
│  │  • Health monitoring                           │    │
│  │  • Audit trail (MongoDB)                       │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Threat Model

| Threat | Mitigation |
|--------|------------|
| **DDoS Attack** | Railway platform protection + Rate limiting |
| **API Abuse** | Payment requirement (Masumi) + Rate limits |
| **Data Breach** | No sensitive data stored, public blockchain only |
| **Credential Theft** | Environment variables, no hardcoded secrets |
| **Man-in-the-Middle** | HTTPS/TLS encryption (automatic) |
| **Injection Attacks** | Pydantic validation, MongoDB parameterization |
| **Service Disruption** | Health checks, auto-restart, fallback strategies |

---

## 📈 Scalability & Performance

### Performance Characteristics

| Metric | Current | Target | Strategy |
|--------|---------|--------|----------|
| **Request Latency** | ~30-45s | <60s | Async operations, caching |
| **Throughput** | 10-20 req/min | 100+ req/min | Horizontal scaling |
| **Concurrent Jobs** | 5-10 | 50+ | Multiple instances |
| **Database Queries** | <100ms | <50ms | Indexes, connection pooling |
| **AI Processing** | 20-30s | <20s | Model optimization |

### Scalability Strategies

#### 1. Horizontal Scaling

```
Current: Single Instance
Future: Multiple Instances + Load Balancer

Benefits:
• Handle more concurrent requests
• Fault tolerance (instance failure)
• Geographic distribution
• Zero-downtime deployments
```

#### 2. Caching Strategy

```python
# Future implementation
from functools import lru_cache
import redis

# In-memory cache for blockchain data
@lru_cache(maxsize=1000)
def get_cached_blockchain_data(wallet_address: str):
    return get_blockchain_data(wallet_address)

# Redis for distributed caching
redis_client = redis.Redis(
    host='redis-host',
    port=6379,
    decode_responses=True
)
```

#### 3. Database Optimization

```
Current Indexes:
• job_id (unique)
• blockchain_identifier

Future Indexes:
• status + created_at (for cleanup)
• identifier_from_purchaser (user queries)
• result_hash (verification)

Connection Pooling:
• Max connections: 50
• Min connections: 10
• Connection timeout: 30s
```

#### 4. Async Processing

```
Current: Sequential AI processing
Future: Parallel agent execution

Benefits:
• Faster analysis (agents run concurrently)
• Better resource utilization
• Reduced latency
```

---

## 🎯 Design Decisions & Trade-offs

### Key Architectural Decisions

#### 1. **FastAPI over Flask/Django**

**Decision:** Use FastAPI for API framework

**Rationale:**
- Native async/await support
- Automatic OpenAPI documentation
- Pydantic validation built-in
- High performance (Starlette + Uvicorn)
- Modern Python 3.11+ features

**Trade-offs:**
-  Better performance
-  Type safety
- ❌ Smaller ecosystem than Flask
- ❌ Steeper learning curve

#### 2. **MongoDB over PostgreSQL**

**Decision:** Use MongoDB for job storage

**Rationale:**
- Flexible schema (JSON documents)
- Easy horizontal scaling
- Native async driver (Motor)
- Good fit for job queue pattern
- Railway integration

**Trade-offs:**
-  Schema flexibility
-  Easy scaling
- ❌ No ACID transactions (not needed)
- ❌ More complex queries

#### 3. **CrewAI over LangChain**

**Decision:** Use CrewAI for multi-agent orchestration

**Rationale:**
- Purpose-built for agent collaboration
- Simpler agent definition
- Better task coordination
- Built on LangChain (best of both)

**Trade-offs:**
-  Cleaner agent code
-  Better collaboration
- ❌ Less flexible than raw LangChain
- ❌ Smaller community

#### 4. **String Result Format over JSON**

**Decision:** Return formatted string for Sokosumi dashboard

**Rationale:**
- Sokosumi dashboard requirement
- Better display formatting
- Human-readable output
- Still store JSON internally

**Trade-offs:**
-  Better UX on dashboard
-  Formatted display
- ❌ Less programmatic access
- ❌ Parsing required for API consumers

#### 5. **Railway over AWS/GCP**

**Decision:** Deploy on Railway platform

**Rationale:**
- Simpler deployment (Git-based)
- Automatic HTTPS/TLS
- Built-in monitoring
- Cost-effective for MVP
- Easy environment management

**Trade-offs:**
-  Faster time to market
-  Lower operational overhead
- ❌ Less control than AWS
- ❌ Vendor lock-in

---

## 🔮 Future Considerations

### Short-term Enhancements (1-3 months)

1. **Rate Limiting**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/start_job")
   @limiter.limit("10/minute")
   async def start_job(...):
       ...
   ```

2. **Caching Layer**
   - Redis for blockchain data caching
   - Reduce Blockfrost API calls
   - Faster response times

3. **Enhanced Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Alert system (PagerDuty/Slack)

4. **API Authentication**
   - API key management
   - JWT tokens
   - Rate limits per user

### Medium-term Enhancements (3-6 months)

1. **Multi-blockchain Support**
   - Ethereum integration
   - Polygon support
   - BSC support

2. **Advanced AI Features**
   - Historical trend analysis
   - Predictive risk scoring
   - Network graph analysis

3. **Microservices Architecture**
   ```
   API Gateway → Auth Service
              → Job Service
              → AI Service
              → Payment Service
   ```

4. **Real-time Updates**
   - WebSocket support
   - Server-Sent Events
   - Live job status updates

### Long-term Vision (6-12 months)

1. **Decentralized Deployment**
   - Multiple node operators
   - Consensus mechanism
   - Distributed AI processing

2. **Machine Learning Pipeline**
   - Custom ML models
   - Training on historical data
   - Continuous improvement

3. **Enterprise Features**
   - White-label solution
   - Custom risk models
   - Batch processing
   - SLA guarantees

4. **Regulatory Compliance**
   - GDPR compliance
   - SOC 2 certification
   - Audit logging
   - Data retention policies

---

## 📚 Related Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Railway deployment instructions
- **[Workflow Documentation](WORKFLOW_DOCUMENTATION.md)** - Technical workflow details
- **[How It Works](HOW_IT_WORKS.md)** - Simple explanation for non-technical users

---

## 📝 Document Metadata

**Version:** 1.0.0  
**Last Updated:** December 7, 2025  
**Authors:** Team X07  
**Status:** Production Ready  
**Review Cycle:** Quarterly

---

**Built with ❤️ by Team X07 for the Cardano Hackathon**

*Making blockchain safer through intelligent risk assessment*


