"""
Masumi Payment Service
Handles payment creation, monitoring, and completion
"""
import uuid
from typing import Dict, Any, Callable, Optional
from masumi.config import Config
from masumi.payment import Payment

from core.logging import get_logger
from core.config import settings

logger = get_logger(__name__)


class MasumiPaymentService:
    """Service for managing Masumi payments"""
    
    def __init__(self):
        """Initialize Masumi payment service"""
        self.config: Optional[Config] = None
        self.payment_instances: Dict[str, Payment] = {}
        logger.info("MasumiPaymentService initialized")
    
    def _ensure_config(self):
        """Lazy-load config when first needed"""
        if self.config is None:
            self.config = Config(
                payment_service_url=settings.payment_service_url,
                payment_api_key=settings.payment_api_key
            )
            logger.info("Masumi config initialized")
    
    async def create_payment_request(
        self,
        job_id: str,
        identifier_from_purchaser: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a payment request for a job
        
        Args:
            job_id: Unique job identifier
            identifier_from_purchaser: Purchaser's identifier
            input_data: Job input data
            
        Returns:
            Payment request data including blockchain identifier
        """
        self._ensure_config()
        logger.info(f"Creating payment request for job {job_id}")
        
        # Create payment instance
        payment = Payment(
            agent_identifier=settings.agent_identifier,
            config=self.config,
            identifier_from_purchaser=identifier_from_purchaser,
            input_data=input_data,
            network=settings.network
        )
        
        # Create payment request
        payment_request = await payment.create_payment_request()
        blockchain_identifier = payment_request["data"]["blockchainIdentifier"]
        payment.payment_ids.add(blockchain_identifier)
        
        # Store payment instance
        self.payment_instances[job_id] = payment
        
        logger.info(f"Payment request created with blockchain ID: {blockchain_identifier}")
        
        return {
            "blockchain_identifier": blockchain_identifier,
            "submit_result_time": payment_request["data"]["submitResultTime"],
            "unlock_time": payment_request["data"]["unlockTime"],
            "external_dispute_unlock_time": payment_request["data"]["externalDisputeUnlockTime"],
            "pay_by_time": payment_request["data"]["payByTime"],
            "input_hash": payment.input_hash
        }
    
    async def start_monitoring(
        self,
        job_id: str,
        callback: Callable[[str], Any]
    ) -> None:
        """
        Start monitoring payment status
        
        Args:
            job_id: Job identifier
            callback: Callback function to call when payment is confirmed
        """
        if job_id not in self.payment_instances:
            logger.error(f"No payment instance found for job {job_id}")
            return
        
        logger.info(f"Starting payment monitoring for job {job_id}")
        await self.payment_instances[job_id].start_status_monitoring(callback)
    
    async def check_payment_status(self, job_id: str) -> Dict[str, Any]:
        """
        Check current payment status
        
        Args:
            job_id: Job identifier
            
        Returns:
            Payment status data
        """
        if job_id not in self.payment_instances:
            logger.warning(f"No payment instance found for job {job_id}")
            return {"status": "unknown"}
        
        try:
            status = await self.payment_instances[job_id].check_payment_status()
            return status
        except Exception as e:
            logger.error(f"Error checking payment status: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def complete_payment(
        self,
        job_id: str,
        payment_id: str,
        result: str
    ) -> Dict[str, Any]:
        """
        Submit result and complete payment
        
        Args:
            job_id: Job identifier
            payment_id: Payment blockchain identifier
            result: Result string to submit
            
        Returns:
            Completion response from Masumi
        """
        if job_id not in self.payment_instances:
            logger.error(f"No payment instance found for job {job_id}")
            raise ValueError(f"No payment instance for job {job_id}")
        
        logger.info(f"Completing payment {payment_id} for job {job_id}")
        logger.info(f"Result length: {len(result)} characters")
        
        completion_response = await self.payment_instances[job_id].complete_payment(
            payment_id,
            result
        )
        
        logger.info(f"Payment completion response: {completion_response}")
        return completion_response
    
    def stop_monitoring(self, job_id: str) -> None:
        """
        Stop monitoring payment status and cleanup
        
        Args:
            job_id: Job identifier
        """
        if job_id in self.payment_instances:
            logger.info(f"Stopping payment monitoring for job {job_id}")
            self.payment_instances[job_id].stop_status_monitoring()
            del self.payment_instances[job_id]
    
    def has_payment_instance(self, job_id: str) -> bool:
        """Check if payment instance exists for job"""
        return job_id in self.payment_instances


# Global payment service instance
payment_service = MasumiPaymentService()


