# 📁 RiskLens AI - Project Structure

**Last Updated:** December 7, 2025  
**Status:** ✅ Modular Architecture Implemented

---

## 🎯 Overview

RiskLens AI now has a **clean modular architecture** with proper separation of concerns. Each component has its own dedicated folder, making the codebase easy to navigate and maintain.

---

## 📂 Complete Directory Structure

```
riskai/
│
├── 📄 main.py                          # Main entry point (FastAPI app)
├── 📄 requirements.txt                 # Python dependencies
├── 📄 runtime.txt                      # Python version for Railway
├── 📄 Dockerfile                       # Docker configuration
├── 📄 deploy.yaml                      # Railway deployment config
├── 📄 README.md                        # Project documentation
│
├── 🤖 agents/                          # AI AGENTS MODULE
│   ├── __init__.py                     # Exports: TransactionAnalyzerAgent, RiskScorerAgent, ComplianceReporterAgent
│   │
│   ├── transaction_analyzer/           # Agent 1: Transaction Analysis
│   │   ├── __init__.py
│   │   └── agent.py                    # Analyzes blockchain transactions
│   │
│   ├── risk_scorer/                    # Agent 2: Risk Scoring
│   │   ├── __init__.py
│   │   └── agent.py                    # Calculates risk scores
│   │
│   └── compliance_reporter/            # Agent 3: Compliance Reporting
│       ├── __init__.py
│       └── agent.py                    # Generates compliance reports
│
├── 🔧 services/                        # BUSINESS SERVICES MODULE
│   ├── __init__.py
│   │
│   ├── blockchain/                     # Blockchain Service
│   │   ├── __init__.py
│   │   ├── analyzer.py                 # Fetches blockchain data (Blockfrost API)
│   │   └── tools.py                    # CrewAI tools for blockchain analysis
│   │
│   ├── payment/                        # Payment Service (Future)
│   │   └── __init__.py                 # Ready for Masumi Network integration
│   │
│   └── storage/                        # Storage Service
│       ├── __init__.py
│       └── mongo_store.py              # MongoDB operations
│
├── ⚙️ core/                            # CORE FRAMEWORK MODULE
│   ├── __init__.py
│   ├── config.py                       # Centralized configuration (Settings class)
│   ├── logging.py                      # Logging setup and configuration
│   └── crew.py                         # RiskAnalysisCrew orchestration
│
├── 🌐 api/                             # API LAYER MODULE
│   ├── __init__.py
│   ├── models.py                       # Pydantic models (StartJobRequest, etc.)
│   ├── formatters.py                   # Result formatting utilities
│   └── routes/                         # API routes (future organization)
│       └── __init__.py
│
├── 📚 docs/                            # DOCUMENTATION
│   ├── README.md                       # Documentation index
│   ├── QUICK_START.md                  # Getting started guide
│   ├── API_REFERENCE.md                # API endpoints documentation
│   ├── DEPLOYMENT_GUIDE.md             # Railway deployment guide
│   ├── ARCHITECTURE.md                 # System architecture
│   ├── HOW_IT_WORKS.md                 # Technical workflow
│   ├── REFACTORING_PLAN.md             # Refactoring implementation plan
│   ├── REFACTORING_SUMMARY.md          # Refactoring completion summary
│   └── PROJECT_STRUCTURE.md            # This file
│
├── 🧪 tests/                           # TESTS (Future)
│   └── __init__.py
│
├── 🛠️ utils/                           # UTILITIES (Future)
│   └── __init__.py
│
└── 📜 OLD FILES (To be removed after testing)
    ├── blockchain_analyzer.py          # → services/blockchain/analyzer.py
    ├── blockchain_tools.py             # → services/blockchain/tools.py
    ├── logging_config.py               # → core/logging.py
    ├── mongo_store.py                  # → services/storage/mongo_store.py
    ├── risk_analysis_crew.py           # → core/crew.py
    ├── crew_definition.py              # Still used (agent registration)
    └── register_agent.py               # Still used (Masumi registration)
```

---

## 🎨 Module Descriptions

### 🤖 Agents Module (`agents/`)
**Purpose:** Contains all AI agents that perform specific analysis tasks

- **Transaction Analyzer** - Analyzes blockchain transactions for patterns
- **Risk Scorer** - Calculates risk scores based on transaction data
- **Compliance Reporter** - Generates compliance reports

**Key Features:**
- Each agent in separate folder
- Easy to add new agents
- Clear agent responsibilities

---

### 🔧 Services Module (`services/`)
**Purpose:** Business logic and external service integrations

#### Blockchain Service (`services/blockchain/`)
- `analyzer.py` - Fetches data from Blockfrost API
- `tools.py` - CrewAI tools for blockchain analysis

#### Storage Service (`services/storage/`)
- `mongo_store.py` - MongoDB operations (save/retrieve analysis results)

#### Payment Service (`services/payment/`)
- Ready for Masumi Network payment integration
- Future implementation

**Key Features:**
- Isolated business logic
- Easy to test
- Clear service boundaries

---

### ⚙️ Core Module (`core/`)
**Purpose:** Core framework components used across the application

- `config.py` - Centralized configuration management
- `logging.py` - Logging setup and utilities
- `crew.py` - CrewAI orchestration and workflow

**Key Features:**
- Shared utilities
- Configuration management
- Framework setup

---

### 🌐 API Module (`api/`)
**Purpose:** API layer components (models, formatters, routes)

- `models.py` - Pydantic models for request/response
- `formatters.py` - Result formatting utilities
- `routes/` - Future API route organization

**Key Features:**
- Clean API contracts
- Request/response validation
- Result formatting

---

## 🔄 Import Examples

### Before Refactoring ❌
```python
from logging_config import setup_logging
from mongo_store import mongo_store
from blockchain_analyzer import BlockchainAnalyzer
from risk_analysis_crew import RiskAnalysisCrew
```

### After Refactoring ✅
```python
from core.logging import setup_logging
from core.config import settings
from core.crew import RiskAnalysisCrew
from services.storage.mongo_store import mongo_store
from services.blockchain.analyzer import BlockchainAnalyzer
from agents import TransactionAnalyzerAgent, RiskScorerAgent, ComplianceReporterAgent
from api.models import StartJobRequest
from api.formatters import format_result_for_display
```

---

## 📊 File Count by Module

| Module | Files | Purpose |
|--------|-------|---------|
| `agents/` | 7 files | AI agent definitions |
| `services/` | 6 files | Business services |
| `core/` | 4 files | Core framework |
| `api/` | 4 files | API layer |
| `docs/` | 9 files | Documentation |
| Root | 6 files | Entry points & config |
| **Total** | **36 files** | Complete application |

---

## 🎯 Benefits of New Structure

### 1. ✅ Clear Organization
- Easy to find specific functionality
- Logical grouping of related code
- Clear module boundaries

### 2. ✅ Better Maintainability
- Easier to modify individual components
- Reduced risk of breaking changes
- Clear dependencies

### 3. ✅ Improved Scalability
- Easy to add new agents
- Simple to add new services
- Clear extension points

### 4. ✅ Team Collaboration
- Multiple developers can work on different modules
- Reduced merge conflicts
- Clear ownership of modules

### 5. ✅ Testing Ready
- Isolated modules for unit testing
- Easier to mock dependencies
- Better test coverage potential

---

## 🚀 Adding New Components

### Adding a New Agent
```bash
# 1. Create agent folder
mkdir -p agents/new_agent

# 2. Create agent files
touch agents/new_agent/__init__.py
touch agents/new_agent/agent.py

# 3. Implement agent in agent.py
# 4. Export in agents/__init__.py
```

### Adding a New Service
```bash
# 1. Create service folder
mkdir -p services/new_service

# 2. Create service files
touch services/new_service/__init__.py
touch services/new_service/service.py

# 3. Implement service logic
# 4. Import in main.py or other modules
```

---

## 📝 Code Standards

### Module Structure
```python
# agents/example_agent/agent.py

from crewai import Agent
from core.logging import get_logger

logger = get_logger(__name__)

class ExampleAgent:
    """Agent description"""
    
    def __init__(self):
        """Initialize agent"""
        pass
    
    def create_agent(self) -> Agent:
        """Create and return CrewAI agent"""
        return Agent(
            role="Example Role",
            goal="Example Goal",
            backstory="Example Backstory",
            verbose=True
        )
```

### Import Order
1. Standard library imports
2. Third-party imports
3. Local application imports

```python
# Standard library
import os
from typing import Dict, List

# Third-party
from crewai import Agent, Task
from pydantic import BaseModel

# Local
from core.logging import get_logger
from services.blockchain.analyzer import BlockchainAnalyzer
```

---

## 🔍 Finding Code

### "Where is the blockchain data fetching code?"
→ `services/blockchain/analyzer.py`

### "Where are the AI agents defined?"
→ `agents/*/agent.py` (each agent in its own folder)

### "Where is the configuration?"
→ `core/config.py`

### "Where is the logging setup?"
→ `core/logging.py`

### "Where is the CrewAI orchestration?"
→ `core/crew.py`

### "Where are the API models?"
→ `api/models.py`

### "Where is MongoDB code?"
→ `services/storage/mongo_store.py`

---

## ✅ Verification Checklist

- [x] All modules created
- [x] All `__init__.py` files present
- [x] Agents separated into folders
- [x] Services organized by type
- [x] Core framework centralized
- [x] API layer separated
- [x] Documentation updated
- [ ] **TODO:** Test imports
- [ ] **TODO:** Test functionality
- [ ] **TODO:** Deploy to Railway
- [ ] **TODO:** Remove old files

---

## 🎓 Architecture Principles

This structure follows:

1. **Separation of Concerns** - Each module has single responsibility
2. **DRY (Don't Repeat Yourself)** - Shared code in core module
3. **SOLID Principles** - Clean architecture patterns
4. **Modularity** - Independent, reusable components
5. **Scalability** - Easy to extend and grow

---

## 📞 Need Help?

- **Finding code?** Use the "Finding Code" section above
- **Adding features?** Follow "Adding New Components" guide
- **Understanding flow?** Check `docs/HOW_IT_WORKS.md`
- **API reference?** See `docs/API_REFERENCE.md`

---

**Built with ❤️ by Team X07**

*Good architecture makes the system easy to understand, easy to develop, easy to maintain, and easy to deploy.* - Robert C. Martin

// Made with Bob
