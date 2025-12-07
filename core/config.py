"""
Configuration Management
Centralized configuration for RiskLens AI
"""
import os
from typing import Optional

class Settings:
    """Application settings loaded from environment variables"""
    
    def __init__(self):
        # API Configuration
        self.api_host: str = os.getenv("API_HOST", "0.0.0.0")
        self.api_port: int = int(os.getenv("API_PORT", "8000"))
        
        # OpenAI Configuration
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        
        # Blockfrost Configuration
        self.blockfrost_project_id: Optional[str] = os.getenv("BLOCKFROST_PROJECT_ID")
        self.network: str = os.getenv("NETWORK", "preprod")
        
        # Masumi Configuration
        self.agent_identifier: str = os.getenv("AGENT_IDENTIFIER", "")
        self.payment_service_url: str = os.getenv("PAYMENT_SERVICE_URL", "")
        self.payment_api_key: str = os.getenv("PAYMENT_API_KEY", "")
        self.seller_vkey: str = os.getenv("SELLER_VKEY", "")
        
        # MongoDB Configuration
        self.mongo_url: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.mongo_db: str = os.getenv("MONGO_DB", "risklens_ai")

# Global settings instance
settings = Settings()

