"""
Job Management Routes
Handles job creation, status checking, and result retrieval
"""
import uuid
import json
from fastapi import APIRouter, HTTPException

from core.logging import get_logger
from core.config import settings
from core.crew import RiskAnalysisCrew
from services.storage.mongo_store import mongo_store
from services.payment.masumi_service import payment_service
from api.models import StartJobRequest
from api.formatters import format_result_for_display

logger = get_logger(__name__)

router = APIRouter()


# ─────────────────────────────────────────────────────────────────────────────
# Helper: Execute CrewAI Task
# ─────────────────────────────────────────────────────────────────────────────
async def execute_crew_task(input_data: dict) -> dict:
    """Execute RiskLens AI analysis for wallet compliance and risk scoring"""
    wallet_address = input_data.get("wallet_address", "")
    logger.info(f"Starting analysis for wallet: {wallet_address}")
    
    crew = RiskAnalysisCrew(logger_instance=logger)
    inputs = {"wallet_address": wallet_address}
    result = crew.crew.kickoff(inputs)
    
    logger.info("Analysis completed successfully")
    
    # Extract the raw result
    result_raw = result.raw if hasattr(result, "raw") else str(result)
    
    # Try to parse as JSON
    try:
        result_dict = json.loads(result_raw)
        return result_dict
    except (json.JSONDecodeError, TypeError):
        logger.warning("Result is not valid JSON, returning as text")
        return {"result": result_raw}


# ─────────────────────────────────────────────────────────────────────────────
# Helper: Handle Payment Callback
# ─────────────────────────────────────────────────────────────────────────────
async def handle_payment_status(job_id: str, payment_id: str) -> None:
    """Executes CrewAI task after payment confirmation"""
    try:
        logger.info(f"Payment callback triggered for job {job_id}")
        
        # Check if job exists
        job = await mongo_store.get_job(job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return
        
        # Update job status to running
        await mongo_store.update_job(job_id, {
            "status": "running",
            "payment_status": "paid"
        })

        # Execute the AI task
        logger.info("Starting CrewAI analysis")
        result_dict = await execute_crew_task(job["input_data"])
        logger.info(f"Analysis completed for job {job_id}")
        
        # Format result
        result_string = format_result_for_display(result_dict)
        
        # Submit result to Masumi
        logger.info(f"Submitting result to Masumi (length: {len(result_string)} chars)")
        
        try:
            completion_response = await payment_service.complete_payment(
                job_id,
                payment_id,
                result_string
            )
            
            # Check if submission was successful
            if completion_response and completion_response.get("status") == "success":
                result_hash = completion_response.get('data', {}).get('resultHash', 'N/A')
                logger.info(f"Result submitted successfully. Hash: {result_hash}")
                
                # Update job status
                await mongo_store.update_job(job_id, {
                    "status": "completed",
                    "payment_status": "result_submitted",
                    "result": result_dict,
                    "result_hash": result_hash
                })
            else:
                logger.error(f"Result submission failed: {completion_response}")
                await mongo_store.update_job(job_id, {
                    "status": "failed",
                    "error": f"Result submission failed: {completion_response}"
                })
                
        except Exception as submit_error:
            logger.error(f"Exception during result submission: {str(submit_error)}")
            await mongo_store.update_job(job_id, {
                "status": "failed",
                "error": f"Result submission error: {str(submit_error)}"
            })
            raise

        # Stop monitoring payment status
        payment_service.stop_monitoring(job_id)
            
    except Exception as e:
        logger.error(f"Error in payment callback for job {job_id}: {str(e)}")
        
        # Update job status
        job = await mongo_store.get_job(job_id)
        if job:
            await mongo_store.update_job(job_id, {
                "status": "failed",
                "error": str(e)
            })
        
        # Stop monitoring
        payment_service.stop_monitoring(job_id)


# ─────────────────────────────────────────────────────────────────────────────
# Route: Start Job (MIP-003: /start_job)
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/start_job")
async def start_job(data: StartJobRequest):
    """Initiates a job and creates a payment request"""
    logger.info("Received start_job request")
    
    try:
        job_id = str(uuid.uuid4())
        wallet_address = data.input_data.get("wallet_address", "")
        
        logger.info(f"Starting job {job_id} for wallet: {wallet_address}")

        # Create payment request
        payment_data = await payment_service.create_payment_request(
            job_id=job_id,
            identifier_from_purchaser=data.identifier_from_purchaser,
            input_data=data.input_data
        )
        
        blockchain_identifier = payment_data["blockchain_identifier"]

        # Store job info in MongoDB
        job_data = {
            "status": "awaiting_payment",
            "payment_status": "pending",
            "blockchain_identifier": blockchain_identifier,
            "input_data": data.input_data,
            "result": None,
            "identifier_from_purchaser": data.identifier_from_purchaser
        }
        await mongo_store.set_job(job_id, job_data)

        # Define payment callback
        async def payment_callback(blockchain_identifier: str):
            await handle_payment_status(job_id, blockchain_identifier)

        # Start monitoring payment status
        logger.info(f"Starting payment monitoring for job {job_id}")
        await payment_service.start_monitoring(job_id, payment_callback)

        # Return response
        return {
            "status": "success",
            "job_id": job_id,
            "blockchainIdentifier": blockchain_identifier,
            "submitResultTime": payment_data["submit_result_time"],
            "unlockTime": payment_data["unlock_time"],
            "externalDisputeUnlockTime": payment_data["external_dispute_unlock_time"],
            "agentIdentifier": settings.agent_identifier,
            "sellerVKey": settings.seller_vkey,
            "identifierFromPurchaser": data.identifier_from_purchaser,
            "input_hash": payment_data["input_hash"],
            "payByTime": payment_data["pay_by_time"],
        }
    except KeyError as e:
        logger.error(f"Missing required field: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Bad Request: Missing or invalid input_data or identifier_from_purchaser"
        )
    except Exception as e:
        logger.error(f"Error in start_job: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Input_data or identifier_from_purchaser is missing, invalid, or does not adhere to the schema."
        )


# ─────────────────────────────────────────────────────────────────────────────
# Route: Check Job Status (MIP-003: /status)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/status")
async def get_status(job_id: str):
    """Retrieves the current status of a specific job"""
    logger.info(f"Checking status for job {job_id}")
    
    # Get job from MongoDB
    job = await mongo_store.get_job(job_id)
    if not job:
        logger.warning(f"Job {job_id} not found")
        raise HTTPException(status_code=404, detail="Job not found")

    # Check latest payment status if payment instance exists
    if payment_service.has_payment_instance(job_id):
        try:
            status = await payment_service.check_payment_status(job_id)
            payment_status = status.get("data", {}).get("status")
            await mongo_store.update_job(job_id, {"payment_status": payment_status})
            job["payment_status"] = payment_status
        except Exception as e:
            logger.error(f"Error checking payment status: {str(e)}")
            job["payment_status"] = "error"

    result_data = job.get("result")
    
    # Format result
    if result_data:
        if isinstance(result_data, dict):
            result = format_result_for_display(result_data)
        elif isinstance(result_data, str):
            result = result_data
        else:
            result = result_data.raw if hasattr(result_data, "raw") else str(result_data)
    else:
        result = None

    return {
        "job_id": job_id,
        "status": job["status"],
        "payment_status": job["payment_status"],
        "result": result
    }

