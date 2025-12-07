import os
import uvicorn
import uuid
import json
from contextlib import asynccontextmanager
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

# ─────────────────────────────────────────────────────────────────────────────
# MongoDB-based distributed job store
# ─────────────────────────────────────────────────────────────────────────────
# Payment instances stored in memory per pod (monitoring is pod-local)
payment_instances = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    await mongo_store.connect()
    logger.info("✅ Application started with MongoDB support")
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
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────
def format_result_for_display(result_dict: dict) -> str:
    """
    Format the JSON result as a nicely formatted string for Sokosumi dashboard display.
    The dashboard only accepts plain strings, not JSON objects.
    """
    if not isinstance(result_dict, dict):
        return str(result_dict)
    
    # Build a formatted string representation
    lines = []
    lines.append("🔍 BLOCKCHAIN WALLET RISK ANALYSIS REPORT")
    lines.append("")
    
    # Wallet Address
    if "wallet_address" in result_dict:
        lines.append(f"📍 Wallet Address: {result_dict['wallet_address']}")
    
    # Analysis Timestamp
    if "analysis_timestamp" in result_dict:
        lines.append(f"📅 Analysis Date: {result_dict['analysis_timestamp']}")
    lines.append("")
    
    # Risk Scores
    lines.append("📊 RISK ASSESSMENT")
    if "risk_score" in result_dict:
        lines.append(f"   Risk Score: {result_dict['risk_score']}/100")
    if "risk_category" in result_dict:
        lines.append(f"   Risk Category: {result_dict['risk_category']}")
    if "trust_score" in result_dict:
        lines.append(f"   Trust Score: {result_dict['trust_score']}/100")
    if "compliance_status" in result_dict:
        lines.append(f"   Compliance Status: {result_dict['compliance_status']}")
    if "confidence_level" in result_dict:
        lines.append(f"   Confidence Level: {result_dict['confidence_level']}")
    lines.append("")
    
    # Executive Summary
    if "executive_summary" in result_dict:
        lines.append("📋 EXECUTIVE SUMMARY")
        lines.append(result_dict['executive_summary'])
        lines.append("")
    
    # Transaction Summary
    if "transaction_summary" in result_dict:
        lines.append("💰 TRANSACTION SUMMARY")
        ts = result_dict['transaction_summary']
        if "total_transactions" in ts:
            lines.append(f"   Total Transactions: {ts['total_transactions']}")
        if "total_volume" in ts:
            lines.append(f"   Total Volume: {ts['total_volume']}")
        if "active_period" in ts:
            lines.append(f"   Active Period: {ts['active_period']}")
        if "counterparties" in ts:
            lines.append(f"   Counterparties: {ts['counterparties']}")
        lines.append("")
    
    # Risk Factors
    if "risk_factors" in result_dict and result_dict['risk_factors']:
        lines.append("⚠️  RISK FACTORS")
        for i, factor in enumerate(result_dict['risk_factors'], 1):
            lines.append(f"\n{i}. {factor.get('factor', 'Unknown Factor')}")
            lines.append(f"   Severity: {factor.get('severity', 'N/A')}")
            lines.append(f"   Description: {factor.get('description', 'N/A')}")
            lines.append(f"   Impact: {factor.get('impact', 'N/A')}")
        lines.append("")
    
    # Suspicious Activities
    if "suspicious_activities" in result_dict:
        lines.append("🚨 SUSPICIOUS ACTIVITIES")
        if result_dict['suspicious_activities']:
            for i, activity in enumerate(result_dict['suspicious_activities'], 1):
                lines.append(f"{i}. {activity}")
        else:
            lines.append("   No suspicious activities detected.")
        lines.append("")
    
    # Recommendations
    if "recommendations" in result_dict and result_dict['recommendations']:
        lines.append("💡 RECOMMENDATIONS")
        for i, rec in enumerate(result_dict['recommendations'], 1):
            lines.append(f"{i}. {rec}")
        lines.append("")
    
    # Report Hash
    if "report_hash" in result_dict:
        lines.append("🔐 VERIFICATION")
        lines.append(f"   Report Hash: {result_dict['report_hash']}")
        lines.append("")
    
    lines.append("End of Report")
    lines.append("")
    lines.append("🌐 Learn more about RiskLens AI:")
    lines.append("   https://studio--studio-2671206846-b156f.us-central1.hosted.app/")
    lines.append("")
    
    return "\n".join(lines)

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
        
        # Format result as a nicely formatted string for Sokosumi dashboard
        result_string = format_result_for_display(result_dict)
        
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
    
    # Format result as nicely formatted string for Sokosumi dashboard
    if result_data:
        if isinstance(result_data, dict):
            # Format the dict as a nice string
            result = format_result_for_display(result_data)
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
    try:
        await mongo_store.ping()  # make a lightweight DB call
        return {"status": "healthy"}
    except Exception:
        return {"status": "unhealthy"}, 503


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
