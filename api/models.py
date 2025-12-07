"""
API Request/Response Models
Pydantic models for API validation
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class StartJobRequest(BaseModel):
    """Request model for /start_job endpoint"""
    identifier_from_purchaser: str
    input_data: Dict[str, str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "identifier_from_purchaser": "exchange_kyc_check_001",
                "input_data": {
                    "wallet_address": "addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgs68faae"
                }
            }
        }

class JobStatusResponse(BaseModel):
    """Response model for /status endpoint"""
    job_id: str
    status: str
    payment_status: str
    result: Optional[str] = None

class HealthResponse(BaseModel):
    """Response model for /health endpoint"""
    status: str
    mongodb: Optional[str] = None

class AvailabilityResponse(BaseModel):
    """Response model for /availability endpoint"""
    status: str
    type: str
    agentIdentifier: str
    message: str

