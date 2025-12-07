"""
Agent Information Routes
Handles agent availability, health checks, and schema information
"""
from fastapi import APIRouter, HTTPException

from core.logging import get_logger
from core.config import settings
from services.storage.mongo_store import mongo_store

logger = get_logger(__name__)

router = APIRouter()


# ─────────────────────────────────────────────────────────────────────────────
# Route: Check Server Availability (MIP-003: /availability)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/availability")
async def check_availability():
    """Checks if the server is operational"""
    agent_id = settings.agent_identifier or "local-dev-agent"
    
    if not settings.agent_identifier:
        logger.warning("AGENT_IDENTIFIER not set, using default for local testing")
    
    logger.info(f"Availability check - Agent Identifier: {agent_id}")
    return {
        "status": "available",
        "type": "masumi-agent",
        "agentIdentifier": agent_id,
        "message": "Server operational."
    }


# ─────────────────────────────────────────────────────────────────────────────
# Route: Retrieve Input Schema (MIP-003: /input_schema)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/input_schema")
async def input_schema():
    """
    Returns the expected input schema for the /start_job endpoint.
    Fulfills MIP-003 /input_schema endpoint.
    """
    return {
        "input_data": [
            {
                "id": "wallet_address",
                "type": "string",
                "name": "Wallet Address",
                "data": {
                    "description": "The blockchain wallet address to analyze for compliance and risk assessment",
                    "placeholder": "Enter wallet address (e.g., addr_test1...)"
                }
            }
        ]
    }


# ─────────────────────────────────────────────────────────────────────────────
# Route: Health Check
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/health")
async def health():
    """Health check endpoint"""
    try:
        await mongo_store.ping()
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


# ─────────────────────────────────────────────────────────────────────────────
# Route: Root Endpoint
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/")
async def root():
    """Root endpoint - redirects to docs"""
    return {
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


