"""
RiskLens AI - Main Entry Point
Blockchain Compliance & Risk Scoring Agent
"""
import os
import sys
import uvicorn
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

# Import from modular structure
from core.logging import setup_logging
from core.config import settings
from core.crew import RiskAnalysisCrew
from services.storage.mongo_store import mongo_store
from api.routes import job_router, agent_router

# Configure logging
logger = setup_logging()

# Load environment variables
load_dotenv(override=True)

logger.info("Application starting")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    await mongo_store.connect()
    logger.info("Application started successfully")
    yield
    # Shutdown
    await mongo_store.disconnect()
    logger.info("Application shutdown complete")


# Initialize FastAPI with lifespan
app = FastAPI(
    title="RiskLens AI - Blockchain Compliance & Risk Scoring Agent",
    description="AI-powered compliance and risk scoring agent for blockchain wallets. Analyzes transactions, detects suspicious patterns, and generates on-chain compliance reports.",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(agent_router, tags=["Agent Info"])
app.include_router(job_router, tags=["Job Management"])


# ─────────────────────────────────────────────────────────────────────────────
# Standalone Mode
# ─────────────────────────────────────────────────────────────────────────────
def main():
    """Run the standalone RiskLens AI agent flow without the API"""
    os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'
    
    print("\n🚀 Running RiskLens AI locally (standalone mode)\n")
    
    # Define test input
    input_data = {
        "wallet_address": "addr_test1qz4x53y7jsfcf7gjc62xljayhyg3yhln6dcuqk09uwrl2txdnlckuxmy084ptm0cxvj7ls72q8kvcpxneektrql3ug0quj6t4n"
    }
    
    print(f"Analyzing Wallet: {input_data['wallet_address']}\n")
    
    # Initialize and run the crew
    crew = RiskAnalysisCrew(verbose=True)
    result = crew.crew.kickoff(inputs=input_data)
    
    # Display the result
    print("\n✅ Risk Analysis Report:\n")
    print(result)
    print()
    
    # Ensure terminal is properly reset
    sys.stdout.flush()
    sys.stderr.flush()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        # Run API mode
        logger.info(f"Starting FastAPI server on {settings.api_host}:{settings.api_port}")
        logger.info(f"API Documentation: http://{settings.api_host}:{settings.api_port}/docs")
        
        uvicorn.run(app, host=settings.api_host, port=settings.api_port, log_level="info")
    else:
        # Run standalone mode
        main()

