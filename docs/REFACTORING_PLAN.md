# 🔄 Codebase Refactoring Plan - Modular Architecture

**Version:** 1.0.0  
**Created:** December 7, 2025  
**Status:** Planning Phase  
**Estimated Effort:** 4-6 hours

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Structure Analysis](#current-structure-analysis)
3. [Proposed Architecture](#proposed-architecture)
4. [Detailed File Organization](#detailed-file-organization)
5. [Migration Steps](#migration-steps)
6. [Import Changes](#import-changes)
7. [Testing Strategy](#testing-strategy)
8. [Benefits & Trade-offs](#benefits--trade-offs)
9. [Implementation Checklist](#implementation-checklist)

---

## 🎯 Executive Summary

### Objective
Refactor the RiskLens AI codebase from a flat structure to a **modular architecture** with clear separation of concerns, making it more maintainable, scalable, and easier to understand.

### Approach
**Modular Structure** - Organize code by functional modules (agents, services, core) with each module containing related components.

### Key Benefits
- ✅ Clear separation of concerns
- ✅ Easier to locate and modify code
- ✅ Better testability (isolated modules)
- ✅ Scalable architecture (easy to add new agents/services)
- ✅ Follows industry best practices
- ✅ Improved code reusability

---

## 📊 Current Structure Analysis

### Current Directory Layout

```
riskai/
├── main.py                      # 581 lines - API endpoints + orchestration
├── risk_analysis_crew.py        # 176 lines - CrewAI setup
├── blockchain_analyzer.py       # 225 lines - Blockfrost integration
├── blockchain_tools.py          # ~100 lines - CrewAI tools
├── mongo_store.py               # ~100 lines - MongoDB operations
├── logging_config.py            # ~50 lines - Logging setup
├── register_agent.py            # Agent registration
├── crew_definition.py           # Crew configuration
├── requirements.txt
├── runtime.txt
├── Dockerfile
├── .env
└── docs/
    ├── ARCHITECTURE.md
    ├── API_REFERENCE.md
    ├── DEPLOYMENT_GUIDE.md
    ├── HOW_IT_WORKS.md
    ├── QUICK_START.md
    ├── README.md
    └── WORKFLOW_DOCUMENTATION.md
```

### Issues with Current Structure

1. **Flat Organization** - All files in root directory
2. **Mixed Concerns** - main.py handles API + orchestration + formatting
3. **Hard to Navigate** - Difficult to find specific functionality
4. **Tight Coupling** - Components not clearly separated
5. **Testing Challenges** - Hard to test individual components
6. **Scalability Issues** - Adding new agents/services clutters root

---

## 🏗️ Proposed Architecture

### New Directory Layout

```
riskai/
├── main.py                          # Entry point (minimal, delegates to modules)
├── requirements.txt
├── runtime.txt
├── Dockerfile
├── .env
├── .gitignore
│
├── agents/                          # AI Agents Module
│   ├── __init__.py
│   ├── base.py                      # Base agent class (if needed)
│   ├── transaction_analyzer/
│   │   ├── __init__.py
│   │   └── agent.py                 # Transaction Analyzer agent
│   ├── risk_scorer/
│   │   ├── __init__.py
│   │   └── agent.py                 # Risk Scorer agent
│   └── compliance_reporter/
│       ├── __init__.py
│       └── agent.py                 # Compliance Reporter agent
│
├── services/                        # Business Services Module
│   ├── __init__.py
│   ├── blockchain/
│   │   ├── __init__.py
│   │   ├── analyzer.py              # BlockchainAnalyzer class
│   │   └── tools.py                 # CrewAI blockchain tools
│   ├── payment/
│   │   ├── __init__.py
│   │   └── masumi_client.py         # Masumi payment integration
│   └── storage/
│       ├── __init__.py
│       └── mongo_store.py           # MongoDB operations
│
├── core/                            # Core Framework Module
│   ├── __init__.py
│   ├── crew.py                      # RiskAnalysisCrew class
│   ├── config.py                    # Configuration management
│   └── logging.py                   # Logging configuration
│
├── api/                             # API Layer Module
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── jobs.py                  # /start_job, /status endpoints
│   │   ├── health.py                # /health, /availability endpoints
│   │   └── schema.py                # /input_schema endpoint
│   ├── models.py                    # Pydantic models
│   ├── dependencies.py              # FastAPI dependencies
│   └── formatters.py                # Result formatting functions
│
├── utils/                           # Utility Functions Module
│   ├── __init__.py
│   └── helpers.py                   # Helper functions
│
├── tests/                           # Test Suite
│   ├── __init__.py
│   ├── test_agents/
│   │   ├── test_transaction_analyzer.py
│   │   ├── test_risk_scorer.py
│   │   └── test_compliance_reporter.py
│   ├── test_services/
│   │   ├── test_blockchain.py
│   │   ├── test_payment.py
│   │   └── test_storage.py
│   ├── test_api/
│   │   └── test_endpoints.py
│   └── conftest.py                  # Pytest configuration
│
└── docs/                            # Documentation
    ├── ARCHITECTURE.md
    ├── API_REFERENCE.md
    ├── DEPLOYMENT_GUIDE.md
    ├── HOW_IT_WORKS.md
    ├── QUICK_START.md
    ├── README.md
    ├── WORKFLOW_DOCUMENTATION.md
    └── REFACTORING_PLAN.md          # This document
```

---

## 📁 Detailed File Organization

### 1. Agents Module (`agents/`)

**Purpose:** Contains all AI agents with clear separation

#### `agents/__init__.py`
```python
"""
AI Agents Module
Contains specialized agents for risk analysis
"""
from agents.transaction_analyzer.agent import TransactionAnalyzerAgent
from agents.risk_scorer.agent import RiskScorerAgent
from agents.compliance_reporter.agent import ComplianceReporterAgent

__all__ = [
    'TransactionAnalyzerAgent',
    'RiskScorerAgent',
    'ComplianceReporterAgent'
]
```

#### `agents/transaction_analyzer/agent.py`
```python
"""
Transaction Analyzer Agent
Analyzes blockchain transactions and identifies patterns
"""
from crewai import Agent
from services.blockchain.tools import BlockchainAnalysisTool

class TransactionAnalyzerAgent:
    """Creates and configures the Transaction Analyzer agent"""
    
    @staticmethod
    def create(verbose: bool = True) -> Agent:
        """Create Transaction Analyzer agent"""
        return Agent(
            role='Blockchain Transaction Analyzer',
            goal='Analyze wallet transactions and identify patterns, anomalies, and suspicious activities',
            backstory="""You are an expert blockchain forensics analyst with deep knowledge of
            transaction patterns, money laundering techniques, and blockchain security. You can
            identify suspicious patterns like mixer usage, rapid transfers, unusual amounts,
            connections to known scam addresses, and other red flags in wallet activity.""",
            tools=[BlockchainAnalysisTool()],
            verbose=verbose
        )
```

#### `agents/risk_scorer/agent.py`
```python
"""
Risk Scorer Agent
Calculates comprehensive risk scores based on transaction analysis
"""
from crewai import Agent

class RiskScorerAgent:
    """Creates and configures the Risk Scorer agent"""
    
    @staticmethod
    def create(verbose: bool = True) -> Agent:
        """Create Risk Scorer agent"""
        return Agent(
            role='Risk Assessment Specialist',
            goal='Calculate comprehensive risk scores based on transaction analysis and behavioral patterns',
            backstory="""You are a risk assessment expert specializing in financial compliance 
            and AML (Anti-Money Laundering) regulations. You evaluate transaction patterns, 
            wallet behavior, and connections to assign accurate risk scores from 0-100, where 
            0 is completely safe and 100 is extremely high risk. You consider factors like 
            transaction frequency, amounts, counterparty risk, and regulatory compliance.""",
            verbose=verbose
        )
```

#### `agents/compliance_reporter/agent.py`
```python
"""
Compliance Reporter Agent
Generates detailed compliance reports with actionable insights
"""
from crewai import Agent

class ComplianceReporterAgent:
    """Creates and configures the Compliance Reporter agent"""
    
    @staticmethod
    def create(verbose: bool = True) -> Agent:
        """Create Compliance Reporter agent"""
        return Agent(
            role='Compliance Report Specialist',
            goal='Generate clear, detailed compliance reports with actionable insights',
            backstory="""You are a compliance documentation expert who creates professional, 
            easy-to-understand reports for regulators, exchanges, and users. You explain 
            complex risk factors in simple terms, provide clear recommendations, and ensure 
            all findings are well-documented and verifiable. Your reports meet international 
            compliance standards and are suitable for on-chain publication.""",
            verbose=verbose
        )
```

---

### 2. Services Module (`services/`)

**Purpose:** Business logic and external service integrations

#### `services/blockchain/analyzer.py`
```python
"""
Blockchain Data Analyzer
Fetches and analyzes blockchain data using Blockfrost API
"""
import os
from typing import Dict, List, Any
from blockfrost import BlockFrostApi, ApiError
from core.logging import get_logger

logger = get_logger(__name__)

class BlockchainAnalyzer:
    """Analyzes blockchain wallet data using Blockfrost API"""
    
    def __init__(self, network: str = "preprod"):
        """Initialize Blockfrost API client"""
        self.network = network
        project_id = os.getenv("BLOCKFROST_PROJECT_ID")
        
        if not project_id:
            logger.warning("BLOCKFROST_PROJECT_ID not set, using mock data")
            self.api = None
        else:
            try:
                self.api = BlockFrostApi(
                    project_id=project_id,
                    base_url=f"https://cardano-{network}.blockfrost.io/api/v0"
                )
                logger.info(f"Blockfrost API initialized for {network}")
            except Exception as e:
                logger.error(f"Failed to initialize Blockfrost: {e}")
                self.api = None
    
    # ... rest of the methods (get_address_info, get_transactions, etc.)
```

#### `services/blockchain/tools.py`
```python
"""
Blockchain Analysis Tools for CrewAI
"""
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import json
from services.blockchain.analyzer import get_blockchain_data

class BlockchainAnalysisInput(BaseModel):
    """Input schema for blockchain analysis tool"""
    wallet_address: str = Field(..., description="The blockchain wallet address to analyze")

class BlockchainAnalysisTool(BaseTool):
    """Tool for analyzing blockchain wallet transactions"""
    name: str = "Blockchain Transaction Analyzer"
    description: str = "Analyzes blockchain wallet transactions and provides detailed risk assessment data"
    args_schema: Type[BaseModel] = BlockchainAnalysisInput
    
    def _run(self, wallet_address: str) -> str:
        """Execute blockchain analysis"""
        data = get_blockchain_data(wallet_address)
        return json.dumps(data, indent=2)
```

#### `services/storage/mongo_store.py`
```python
"""
MongoDB Storage Service
Handles persistent job storage
"""
import os
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING
from core.logging import get_logger

logger = get_logger(__name__)

class MongoStore:
    """MongoDB storage for job data"""
    
    def __init__(self):
        """Initialize MongoDB store"""
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.jobs_collection = None
    
    async def connect(self) -> None:
        """Connect to MongoDB"""
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB", "risklens_ai")
        
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]
        self.jobs_collection = self.db.jobs
        
        # Create indexes
        await self._create_indexes()
        logger.info(f"Connected to MongoDB: {db_name}")
    
    # ... rest of the methods
```

#### `services/payment/masumi_client.py`
```python
"""
Masumi Payment Service Client
Handles payment processing via Masumi Network
"""
import os
from typing import Dict, Any, Callable
from masumi.config import Config
from masumi.payment import Payment
from core.logging import get_logger

logger = get_logger(__name__)

class MasumiClient:
    """Client for Masumi payment processing"""
    
    def __init__(self):
        """Initialize Masumi client"""
        self.config = Config(
            payment_service_url=os.getenv("PAYMENT_SERVICE_URL"),
            payment_api_key=os.getenv("PAYMENT_API_KEY")
        )
        self.network = os.getenv("NETWORK", "preprod")
        logger.info("Masumi client initialized")
    
    def create_payment(
        self,
        agent_identifier: str,
        identifier_from_purchaser: str,
        input_data: Dict[str, Any]
    ) -> Payment:
        """Create a new payment instance"""
        return Payment(
            agent_identifier=agent_identifier,
            config=self.config,
            identifier_from_purchaser=identifier_from_purchaser,
            input_data=input_data,
            network=self.network
        )
    
    # ... additional payment methods
```

---

### 3. Core Module (`core/`)

**Purpose:** Core framework components

#### `core/crew.py`
```python
"""
RiskLens AI Crew
Orchestrates multiple agents for risk analysis
"""
from crewai import Crew, Task
from agents import TransactionAnalyzerAgent, RiskScorerAgent, ComplianceReporterAgent
from core.logging import get_logger

logger = get_logger(__name__)

class RiskAnalysisCrew:
    """RiskLens AI - Blockchain Compliance & Risk Scoring Agent"""
    
    def __init__(self, verbose: bool = True):
        """Initialize the crew"""
        self.verbose = verbose
        self.logger = logger
        self.crew = self._create_crew()
        logger.info("RiskAnalysisCrew initialized")
    
    def _create_crew(self) -> Crew:
        """Create the crew with agents and tasks"""
        # Create agents
        transaction_analyzer = TransactionAnalyzerAgent.create(self.verbose)
        risk_scorer = RiskScorerAgent.create(self.verbose)
        compliance_reporter = ComplianceReporterAgent.create(self.verbose)
        
        # Create tasks
        tasks = self._create_tasks(
            transaction_analyzer,
            risk_scorer,
            compliance_reporter
        )
        
        # Create crew
        return Crew(
            agents=[transaction_analyzer, risk_scorer, compliance_reporter],
            tasks=tasks
        )
    
    def _create_tasks(self, *agents) -> list[Task]:
        """Create tasks for the crew"""
        # ... task definitions
        pass
```

#### `core/config.py`
```python
"""
Configuration Management
Centralized configuration for the application
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # OpenAI Configuration
    openai_api_key: str
    
    # Blockfrost Configuration
    blockfrost_project_id: Optional[str] = None
    network: str = "preprod"
    
    # Masumi Configuration
    agent_identifier: str
    payment_service_url: str
    payment_api_key: str
    seller_vkey: str
    
    # MongoDB Configuration
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "risklens_ai"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

#### `core/logging.py`
```python
"""
Logging Configuration
Centralized logging setup
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging() -> logging.Logger:
    """Setup application logging"""
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger("risklens_ai")
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = RotatingFileHandler(
        log_dir / "risklens_ai.log",
        maxBytes=10_000_000,
        backupCount=5
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler (for Railway)
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(f"risklens_ai.{name}")
```

---

### 4. API Module (`api/`)

**Purpose:** API layer with routes and models

#### `api/routes/jobs.py`
```python
"""
Job Management Routes
Handles /start_job and /status endpoints
"""
from fastapi import APIRouter, HTTPException
from api.models import StartJobRequest, JobStatusResponse
from api.formatters import format_result_for_display
from services.payment.masumi_client import MasumiClient
from services.storage.mongo_store import mongo_store
from core.crew import RiskAnalysisCrew
from core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/start_job")
async def start_job(data: StartJobRequest):
    """Initiate a new risk analysis job"""
    # Implementation here
    pass

@router.get("/status")
async def get_status(job_id: str) -> JobStatusResponse:
    """Get job status"""
    # Implementation here
    pass
```

#### `api/routes/health.py`
```python
"""
Health Check Routes
Handles /health and /availability endpoints
"""
from fastapi import APIRouter, HTTPException
from services.storage.mongo_store import mongo_store
from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/health")
async def health():
    """Health check endpoint"""
    try:
        await mongo_store.ping()
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@router.get("/availability")
async def check_availability():
    """Check agent availability"""
    return {
        "status": "available",
        "type": "masumi-agent",
        "agentIdentifier": settings.agent_identifier,
        "message": "Server operational."
    }
```

#### `api/models.py`
```python
"""
API Request/Response Models
Pydantic models for API validation
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class StartJobRequest(BaseModel):
    """Request model for /start_job"""
    identifier_from_purchaser: str
    input_data: Dict[str, str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "identifier_from_purchaser": "exchange_kyc_001",
                "input_data": {
                    "wallet_address": "addr_test1..."
                }
            }
        }

class JobStatusResponse(BaseModel):
    """Response model for /status"""
    job_id: str
    status: str
    payment_status: str
    result: Optional[str] = None
```

#### `api/formatters.py`
```python
"""
Result Formatters
Format analysis results for different outputs
"""
from typing import Dict, Any

def format_result_for_display(result_dict: Dict[str, Any]) -> str:
    """
    Format the JSON result as a nicely formatted string for Sokosumi dashboard.
    The dashboard only accepts plain strings, not JSON objects.
    """
    if not isinstance(result_dict, dict):
        return str(result_dict)
    
    lines = []
    lines.append("🔍 BLOCKCHAIN WALLET RISK ANALYSIS REPORT")
    lines.append("")
    
    # ... rest of formatting logic
    
    return "\n".join(lines)
```

---

### 5. Main Entry Point (`main.py`)

**Purpose:** Minimal entry point that delegates to modules

```python
"""
RiskLens AI - Main Entry Point
Blockchain Compliance & Risk Scoring Agent
"""
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

from core.config import settings
from core.logging import setup_logging
from services.storage.mongo_store import mongo_store
from api.routes import jobs, health, schema

# Load environment variables
load_dotenv(override=True)

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await mongo_store.connect()
    logger.info("✅ Application started")
    yield
    # Shutdown
    await mongo_store.disconnect()
    logger.info("Application shutdown complete")

# Initialize FastAPI
app = FastAPI(
    title="RiskLens AI - Blockchain Compliance & Risk Scoring Agent",
    description="AI-powered compliance and risk scoring agent for blockchain wallets",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(jobs.router, tags=["Jobs"])
app.include_router(health.router, tags=["Health"])
app.include_router(schema.router, tags=["Schema"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RiskLens AI - Blockchain Compliance & Risk Scoring Agent",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        uvicorn.run(
            app,
            host=settings.api_host,
            port=settings.api_port,
            log_level="info"
        )
```

---

## 🔄 Migration Steps

### Phase 1: Preparation (30 minutes)

1. **Create Branch**
   ```bash
   git checkout -b refactor/modular-architecture
   ```

2. **Backup Current Code**
   ```bash
   cp -r riskai riskai_backup
   ```

3. **Create New Directory Structure**
   ```bash
   mkdir -p agents/{transaction_analyzer,risk_scorer,compliance_reporter}
   mkdir -p services/{blockchain,payment,storage}
   mkdir -p core
   mkdir -p api/routes
   mkdir -p utils
   mkdir -p tests/{test_agents,test_services,test_api}
   ```

4. **Create `__init__.py` Files**
   ```bash
   touch agents/__init__.py
   touch agents/transaction_analyzer/__init__.py
   touch agents/risk_scorer/__init__.py
   touch agents/compliance_reporter/__init__.py
   touch services/__init__.py
   touch services/blockchain/__init__.py
   touch services/payment/__init__.py
   touch services/storage/__init__.py
   touch core/__init__.py
   touch api/__init__.py
   touch api/routes/__init__.py
   touch utils/__init__.py
   touch tests/__init__.py
   ```

### Phase 2: Move and Refactor Files (2-3 hours)

1. **Move Blockchain Services**
   ```bash
   # Move and rename
   mv blockchain_analyzer.py services/blockchain/analyzer.py
   mv blockchain_tools.py services/blockchain/tools.py
   
   # Update imports in both files
   # analyzer.py: from core.logging import get_logger
   # tools.py: from services.blockchain.analyzer import get_blockchain_data
   ```

2. **Move Storage Service**
   ```bash
   mv mongo_store.py services/storage/mongo_store.py
   # Update imports: from core.logging import get_logger
   ```

3. **Move Core Components**
   ```bash
   mv logging_config.py core/logging.py
   # Create core/config.py (new file)
   # Move crew logic from risk_analysis_crew.py to core/crew.py
   ```

4. **Create Agent Files**
   - Extract agent definitions from `risk_analysis_crew.py`
   - Create separate files for each agent
   - Update imports

5. **Create API Module**
   - Extract routes from `main.py`
   - Create separate route files
   - Create models.py and formatters.py
   - Update main.py to be minimal entry point

6. **Create Payment Service**
   - Extract Masumi payment logic from main.py
   - Create services/payment/masumi_client.py

### Phase 3: Update Imports (1 hour)

Update all import statements across the codebase:

**Old imports:**
```python
from blockchain_analyzer import BlockchainAnalyzer
from mongo_store import mongo_store
from logging_config import setup_logging
from risk_analysis_crew import RiskAnalysisCrew
```

**New imports:**
```python
from services.blockchain.analyzer import BlockchainAnalyzer
from services.storage.mongo_store import mongo_store
from core.logging import setup_logging
from core.crew import RiskAnalysisCrew
from agents import TransactionAnalyzerAgent, RiskScorerAgent, ComplianceReporterAgent
```

### Phase 4: Testing (1-2 hours)

1. **Unit Tests**
   ```bash
   pytest tests/test_services/
   pytest tests/test_agents/
   ```

2. **Integration Tests**
   ```bash
   pytest tests/test_api/
   ```

3. **Manual Testing**
   ```bash
   python main.py api
   # Test all endpoints
   ```

### Phase 5: Documentation Update (30 minutes)

1. Update README.md with new structure
2. Update ARCHITECTURE.md
3. Update QUICK_START.md
4. Add migration notes

### Phase 6: Deployment (30 minutes)

1. **Test Locally**
   ```bash
   python main.py api
   ```

2. **Deploy to Railway**
   ```bash
   git add .
   git commit -m "Refactor: Implement modular architecture"
   git push origin refactor/modular-architecture
   ```

3. **Verify Deployment**
   - Check Railway logs
   - Test all endpoints
   - Verify MongoDB connection

---

## 📝 Import Changes

### Summary of Import Changes

| Old Import | New Import |
|------------|------------|
| `from blockchain_analyzer import BlockchainAnalyzer` | `from services.blockchain.analyzer import BlockchainAnalyzer` |
| `from blockchain_tools import BlockchainAnalysisTool` | `from services.blockchain.tools import BlockchainAnalysisTool` |
| `from mongo_store import mongo_store` | `from services.storage.mongo_store import mongo_store` |
| `from logging_config import setup_logging` | `from core.logging import setup_logging` |
| `from risk_analysis_crew import RiskAnalysisCrew` | `from core.crew import RiskAnalysisCrew` |
| N/A | `from agents import TransactionAnalyzerAgent` |
| N/A | `from services.payment.masumi_client import MasumiClient` |
| N/A | `from core.config import settings` |

---

## 🧪 Testing Strategy

### Unit Tests

```python
# tests/test_agents/test_transaction_analyzer.py
def test_transaction_analyzer_creation():
    """Test agent creation"""
    agent = TransactionAnalyzerAgent.create()
    assert agent.role == 'Blockchain Transaction Analyzer'

# tests/test_services/test_blockchain.py
def test_blockchain_analyzer_init():
    """Test BlockchainAnalyzer initialization"""
    analyzer = BlockchainAnalyzer(network="preprod")
    assert analyzer.network == "preprod"

# tests/test_api/test_endpoints.py
async def test_health_endpoint(client):
    """Test health endpoint"""
    response = await client.get("/health")
    assert response.status_code == 200
```

### Integration Tests

```python
# tests/test_api/test_job_flow.py
async def test_complete_job_flow(client):
    """Test complete job flow"""
    # 1. Start job
    response = await client.post("/start_job", json={...})
    job_id = response.json()["job_id"]
    
    # 2. Check status
    response = await client.get(f"/status?job_id={job_id}")
    assert response.json()["status"] in ["awaiting_payment", "running"]
```

---

## ⚖️ Benefits & Trade-offs

### Benefits

✅ **Clear Organization**
- Easy to find specific functionality
- Logical grouping of related code
- Clear module boundaries

✅ **Better Maintainability**
- Easier to modify individual components
- Reduced risk of breaking changes
- Clear dependencies

✅ **Improved Testability**
- Isolated modules for unit testing
- Easier to mock dependencies
- Better test coverage

✅ **Scalability**
- Easy to add new agents
- Simple to add new services
- Clear extension points

✅ **Team Collaboration**
- Multiple developers can work on different modules
- Reduced merge conflicts
- Clear ownership of modules

✅ **Code Reusability**
- Services can be reused across agents
- Utilities available to all modules
- Shared core components

### Trade-offs

⚠️ **Initial Effort**
- Time required for refactoring (4-6 hours)
- Need to update all imports
- Testing required

⚠️ **Import Complexity**
- Longer import paths
- Need to understand module structure
- More `__init__.py` files

⚠️ **Learning Curve**
- New developers need to learn structure
- Documentation must be updated
- Onboarding takes slightly longer

### Mitigation Strategies

1. **Good Documentation** - Clear README and architecture docs
2. **Consistent Naming** - Follow naming conventions
3. **IDE Support** - Use IDE auto-import features
4. **Gradual Migration** - Can be done incrementally if needed

---

## ✅ Implementation Checklist

### Pre-Migration
- [ ] Create feature branch
- [ ] Backup current code
- [ ] Review current dependencies
- [ ] Plan downtime (if needed)

### Directory Structure
- [ ] Create all directories
- [ ] Create all `__init__.py` files
- [ ] Set up proper Python path

### File Migration
- [ ] Move blockchain_analyzer.py → services/blockchain/analyzer.py
- [ ] Move blockchain_tools.py → services/blockchain/tools.py
- [ ] Move mongo_store.py → services/storage/mongo_store.py
- [ ] Move logging_config.py → core/logging.py
- [ ] Create core/config.py
- [ ] Create core/crew.py
- [ ] Create agent files (3 agents)
- [ ] Create API route files
- [ ] Create api/models.py
- [ ] Create api/formatters.py
- [ ] Create services/payment/masumi_client.py
- [ ] Update main.py

### Import Updates
- [ ] Update imports in all agent files
- [ ] Update imports in all service files
- [ ] Update imports in core files
- [ ] Update imports in API files
- [ ] Update imports in main.py

### Testing
- [ ] Write unit tests for agents
- [ ] Write unit tests for services
- [ ] Write integration tests for API
- [ ] Run all tests locally
- [ ] Fix any failing tests

### Documentation
- [ ] Update README.md
- [ ] Update ARCHITECTURE.md
- [ ] Update QUICK_START.md
- [ ] Add migration notes
- [ ] Update code comments

### Deployment
- [ ] Test locally
- [ ] Commit changes
- [ ] Push to repository
- [ ] Deploy to Railway
- [ ] Verify deployment
- [ ] Test all endpoints
- [ ] Monitor logs

### Post-Migration
- [ ] Update team documentation
- [ ] Notify team members
- [ ] Archive old code
- [ ] Delete backup (after verification)

---

## 📞 Support & Questions

If you encounter issues during migration:

1. **Check Logs** - Review application logs for errors
2. **Verify Imports** - Ensure all imports are updated
3. **Test Incrementally** - Test each module as you migrate
4. **Rollback Plan** - Keep backup until fully verified

---

## 📚 Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [QUICK_START.md](QUICK_START.md) - Getting started guide
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment instructions

---

**Created by:** Team X07  
**Status:** Ready for Implementation  
**Estimated Completion:** 4-6 hours

---

**Next Steps:**
1. Review this plan with the team
2. Schedule migration window
3. Create feature branch
4. Begin Phase 1: Preparation


