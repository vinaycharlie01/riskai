import os
import uvicorn
import uuid
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field, field_validator
from masumi.config import Config
from masumi.payment import Payment
from risk_analysis_crew import RiskAnalysisCrew
from logging_config import setup_logging
from mongo_store import mongo_store

# Configure logging
logger = setup_logging()

# Load environment variables
load_dotenv(override=True)

# Retrieve API Keys and URLs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL")
PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")
NETWORK = os.getenv("NETWORK")

logger.info("Starting application with configuration:")
logger.info(f"PAYMENT_SERVICE_URL: {PAYMENT_SERVICE_URL}")

# Initialize FastAPI
app = FastAPI(
    title="RiskLens AI - Blockchain Compliance & Risk Scoring Agent",
    description="AI-powered compliance and risk scoring agent for blockchain wallets. Analyzes transactions, detects suspicious patterns, and generates on-chain compliance reports.",
    version="1.0.0"
)

# ─────────────────────────────────────────────────────────────────────────────
# MongoDB-based distributed job store
# ─────────────────────────────────────────────────────────────────────────────
# Payment instances stored in memory per pod (monitoring is pod-local)
payment_instances = {}

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    await mongo_store.connect()
    logger.info("✅ Application started with MongoDB support")

@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from MongoDB on shutdown"""
    await mongo_store.disconnect()
    logger.info("Application shutdown complete")

# ─────────────────────────────────────────────────────────────────────────────
# Initialize Masumi Payment Config
# ─────────────────────────────────────────────────────────────────────────────
config = Config(
    payment_service_url=PAYMENT_SERVICE_URL,
    payment_api_key=PAYMENT_API_KEY
)

# ─────────────────────────────────────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────────────────────────────────────
class StartJobRequest(BaseModel):
    identifier_from_purchaser: str
    input_data: dict[str, str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "identifier_from_purchaser": "exchange_kyc_check_001",
                "input_data": {
                    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
                }
            }
        }

class ProvideInputRequest(BaseModel):
    job_id: str

# ─────────────────────────────────────────────────────────────────────────────
# CrewAI Task Execution
# ─────────────────────────────────────────────────────────────────────────────
async def execute_crew_task(input_data: dict) -> dict:
    """ Execute RiskLens AI analysis for wallet compliance and risk scoring """
    wallet_address = input_data.get("wallet_address", "")
    logger.info(f"Starting RiskLens AI analysis for wallet: {wallet_address}")
    
    crew = RiskAnalysisCrew(logger=logger)
    inputs = {"wallet_address": wallet_address}
    result = crew.crew.kickoff(inputs)
    
    logger.info("RiskLens AI analysis completed successfully")
    
    # Extract the raw result (which should be a JSON string from the Compliance Reporter)
    result_raw = result.raw if hasattr(result, "raw") else str(result)
    
    # Try to parse as JSON, if it fails, return as plain text
    try:
        result_dict = json.loads(result_raw)
        return result_dict
    except (json.JSONDecodeError, TypeError):
        logger.warning("Result is not valid JSON, returning as text")
        return {"result": result_raw}

# ─────────────────────────────────────────────────────────────────────────────
# 1) Start Job (MIP-003: /start_job)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/start_job")
async def start_job(data: StartJobRequest):
    """ Initiates a job and creates a payment request """
    logger.info(f"Received start_job request")
    logger.info(f"Input data: {data.input_data}")
    try:
        job_id = str(uuid.uuid4())
        agent_identifier = os.getenv("AGENT_IDENTIFIER")
        
        # Log the wallet address
        wallet_address = data.input_data.get("wallet_address", "")
        logger.info(f"Received risk analysis request for wallet: {wallet_address}")
        logger.info(f"Starting job {job_id} with agent {agent_identifier}")

        # Create a payment request using Masumi
        # Note: Payment amount is configured at agent registration level
        payment = Payment(
            agent_identifier=agent_identifier,
            config=config,
            identifier_from_purchaser=data.identifier_from_purchaser,
            input_data=data.input_data,
            network=NETWORK
        )
        
        logger.info(f"Creating payment request for agent: {agent_identifier}")
        payment_request = await payment.create_payment_request()
        blockchain_identifier = payment_request["data"]["blockchainIdentifier"]
        payment.payment_ids.add(blockchain_identifier)
        logger.info(f"Created payment request with blockchain identifier: {blockchain_identifier}")

        # Store job info in MongoDB (Awaiting payment)
        job_data = {
            "status": "awaiting_payment",
            "payment_status": "pending",
            "blockchain_identifier": blockchain_identifier,
            "input_data": data.input_data,
            "result": None,
            "identifier_from_purchaser": data.identifier_from_purchaser
        }
        await mongo_store.set_job(job_id, job_data)

        async def payment_callback(blockchain_identifier: str):
            logger.info(f"🔔 Payment callback triggered for job {job_id}, payment {blockchain_identifier}")
            await handle_payment_status(job_id, blockchain_identifier)

        # Start monitoring the payment status (pod-local)
        payment_instances[job_id] = payment
        logger.info(f"Starting payment status monitoring for job {job_id}")
        logger.info(f"Monitoring payment ID: {blockchain_identifier}")
        await payment.start_status_monitoring(payment_callback)

        # Return the response in the required format
        return {
            "status": "success",
            "job_id": job_id,
            "blockchainIdentifier": blockchain_identifier,
            "submitResultTime": payment_request["data"]["submitResultTime"],
            "unlockTime": payment_request["data"]["unlockTime"],
            "externalDisputeUnlockTime": payment_request["data"]["externalDisputeUnlockTime"],
            "agentIdentifier": agent_identifier,
            "sellerVKey": os.getenv("SELLER_VKEY"),
            "identifierFromPurchaser": data.identifier_from_purchaser,
            "input_hash": payment.input_hash,
            "payByTime": payment_request["data"]["payByTime"],
        }
    except KeyError as e:
        logger.error(f"Missing required field in request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail="Bad Request: If input_data or identifier_from_purchaser is missing, invalid, or does not adhere to the schema."
        )
    except Exception as e:
        logger.error(f"Error in start_job: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail="Input_data or identifier_from_purchaser is missing, invalid, or does not adhere to the schema."
        )

# ─────────────────────────────────────────────────────────────────────────────
# 2) Process Payment and Execute AI Task
# ─────────────────────────────────────────────────────────────────────────────
async def handle_payment_status(job_id: str, payment_id: str) -> None:
    """ Executes CrewAI task after payment confirmation """
    try:
        logger.info(f"=" * 70)
        logger.info(f"🎯 PAYMENT CALLBACK TRIGGERED")
        logger.info(f"Job ID: {job_id}")
        logger.info(f"Payment ID: {payment_id}")
        logger.info(f"=" * 70)
        
        # Check if job exists in MongoDB
        job = await mongo_store.get_job(job_id)
        if not job:
            logger.error(f"❌ Job {job_id} not found in MongoDB!")
            return
        
        logger.info(f"✅ Job found, starting AI analysis...")
        
        # Update job status to running
        await mongo_store.update_job(job_id, {
            "status": "running",
            "payment_status": "paid"
        })
        logger.info(f"Input data: {job['input_data']}")

        # Execute the AI task
        logger.info(f"🤖 Starting CrewAI analysis...")
        result_dict = await execute_crew_task(job["input_data"])
        logger.info(f"✅ Crew task completed for job {job_id}")
        
        # Convert result dict to JSON string for Masumi
        result_string = json.dumps(result_dict, indent=2)
        
        # Log the result for debugging
        logger.info(f"Result type: {type(result_string)}")
        logger.info(f"Result length: {len(result_string)} characters")
        logger.info(f"Result preview (first 500 chars): {result_string[:500]}")
        
        # Submit result to Masumi
        logger.info(f"📤 Sending result to Masumi for payment {payment_id}")
        logger.info(f"Using payment instance: {payment_instances[job_id]}")
        
        try:
            completion_response = await payment_instances[job_id].complete_payment(payment_id, result_string)
            logger.info(f"✅ Masumi API response: {json.dumps(completion_response, indent=2)}")
            
            # Check if submission was successful
            if completion_response and completion_response.get("status") == "success":
                logger.info(f"✅ Result successfully submitted to Masumi!")
                result_hash = completion_response.get('data', {}).get('resultHash', 'N/A')
                logger.info(f"Result hash: {result_hash}")
                logger.info(f"Result will be verified on-chain within 1-2 minutes")
                
                # Update job status in MongoDB
                await mongo_store.update_job(job_id, {
                    "status": "completed",
                    "payment_status": "result_submitted",
                    "result": result_dict,
                    "result_hash": result_hash
                })
            else:
                logger.error(f"❌ Result submission failed!")
                logger.error(f"Response: {completion_response}")
                await mongo_store.update_job(job_id, {
                    "status": "failed",
                    "error": f"Result submission failed: {completion_response}"
                })
                
        except Exception as submit_error:
            logger.error(f"❌ Exception during result submission: {str(submit_error)}", exc_info=True)
            await mongo_store.update_job(job_id, {
                "status": "failed",
                "error": f"Result submission error: {str(submit_error)}"
            })
            raise

        # Stop monitoring payment status
        if job_id in payment_instances:
            payment_instances[job_id].stop_status_monitoring()
            del payment_instances[job_id]
            
    except Exception as e:
        logger.error(f"=" * 70)
        logger.error(f"❌ ERROR IN PAYMENT CALLBACK")
        logger.error(f"Job ID: {job_id}")
        logger.error(f"Payment ID: {payment_id}")
        logger.error(f"Error: {str(e)}")
        logger.error(f"=" * 70, exc_info=True)
        
        # Update job status in MongoDB
        job = await mongo_store.get_job(job_id)
        if job:
            await mongo_store.update_job(job_id, {
                "status": "failed",
                "error": str(e)
            })
        
        # Still stop monitoring to prevent repeated failures
        if job_id in payment_instances:
            payment_instances[job_id].stop_status_monitoring()
            del payment_instances[job_id]

# ─────────────────────────────────────────────────────────────────────────────
# 3) Check Job and Payment Status (MIP-003: /status)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/status")
async def get_status(job_id: str):
    """ Retrieves the current status of a specific job """
    logger.info(f"Checking status for job {job_id}")
    
    # Get job from MongoDB
    job = await mongo_store.get_job(job_id)
    if not job:
        logger.warning(f"Job {job_id} not found in MongoDB")
        raise HTTPException(status_code=404, detail="Job not found")

    # Check latest payment status if payment instance exists (pod-local)
    if job_id in payment_instances:
        try:
            status = await payment_instances[job_id].check_payment_status()
            payment_status = status.get("data", {}).get("status")
            # Update in MongoDB
            await mongo_store.update_job(job_id, {"payment_status": payment_status})
            job["payment_status"] = payment_status
            logger.info(f"Updated payment status for job {job_id}: {payment_status}")
        except ValueError as e:
            logger.warning(f"Error checking payment status: {str(e)}")
            job["payment_status"] = "unknown"
        except Exception as e:
            logger.error(f"Error checking payment status: {str(e)}", exc_info=True)
            job["payment_status"] = "error"

    result_data = job.get("result")
    logger.info(f"Result data type: {type(result_data)}")
    
    # Format result as plain string (not JSON) for Sokosumi
    if result_data:
        if isinstance(result_data, dict):
            # Convert dict to plain string
            result = str(result_data)
        elif isinstance(result_data, str):
            # Already a string
            result = result_data
        else:
            # It's a CrewOutput or other object
            result = result_data.raw if hasattr(result_data, "raw") else str(result_data)
    else:
        result = None

    return {
        "job_id": job_id,
        "status": job["status"],
        "payment_status": job["payment_status"],
        "result": result
    }

# ─────────────────────────────────────────────────────────────────────────────
# 4) Check Server Availability (MIP-003: /availability)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/availability")
async def check_availability():
    """ Checks if the server is operational """
    agent_identifier = os.getenv("AGENT_IDENTIFIER")
    
    if not agent_identifier:
        logger.error("AGENT_IDENTIFIER environment variable is not set!")
        raise HTTPException(status_code=500, detail="Agent identifier not configured")
    
    logger.info(f"Availability check - Agent Identifier: {agent_identifier}")
    return {
        "status": "available",
        "type": "masumi-agent",
        "agentIdentifier": agent_identifier,
        "message": "Server operational."
    }

# ─────────────────────────────────────────────────────────────────────────────
# 5) Retrieve Input Schema (MIP-003: /input_schema)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/input_schema")
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
                    "placeholder": "Enter wallet address (e.g., 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb)"
                }
            }
        ]
    }

# ─────────────────────────────────────────────────────────────────────────────
# 6) Health Check
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    """
    Returns the health of the server.
    """
    return {
        "status": "healthy"
    }

# ─────────────────────────────────────────────────────────────────────────────
# Main Logic if Called as a Script
# ─────────────────────────────────────────────────────────────────────────────
def main():
    """Run the standalone RiskLens AI agent flow without the API"""
    import os
    # Disable execution traces to avoid terminal issues
    os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'
    
    print("\n" + "=" * 70)
    print("🚀 Running RiskLens AI locally (standalone mode)...")
    print("=" * 70 + "\n")
    
    # Define test input - sample wallet address
    input_data = {"wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"}
    
    print(f"Analyzing Wallet: {input_data['wallet_address']}")
    print("\nProcessing with RiskLens AI agents...\n")
    
    # Initialize and run the crew
    crew = RiskAnalysisCrew(verbose=True)
    result = crew.crew.kickoff(inputs=input_data)
    
    # Display the result
    print("\n" + "=" * 70)
    print("✅ Risk Analysis Report:")
    print("=" * 70 + "\n")
    print(result)
    print("\n" + "=" * 70 + "\n")
    
    # Ensure terminal is properly reset after CrewAI execution
    import sys
    sys.stdout.flush()
    sys.stderr.flush()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "api":
        # Run API mode
        port = int(os.environ.get("API_PORT", 8000))
        # Set host from environment variable, default to localhost for security.
        # Use host=0.0.0.0 to allow external connections (e.g., in Docker or production).
        host = os.environ.get("API_HOST", "0.0.0.0")

        print("\n" + "=" * 70)
        print("🚀 Starting FastAPI server with Masumi integration...")
        print("=" * 70)
        print(f"API Documentation:        http://{host}:{port}/docs")
        print(f"Availability Check:       http://{host}:{port}/availability")
        print(f"Status Check:             http://{host}:{port}/status")
        print(f"Input Schema:             http://{host}:{port}/input_schema\n")
        print("=" * 70 + "\n")

        uvicorn.run(app, host=host, port=port, log_level="info")
    else:
        # Run standalone mode
        main()

# Made with Bob
