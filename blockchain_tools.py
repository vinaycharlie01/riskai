"""
Custom tools for CrewAI agents to interact with blockchain data
"""
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from blockchain_analyzer import get_blockchain_data
import json

class BlockchainAnalysisInput(BaseModel):
    """Input schema for blockchain analysis tool"""
    wallet_address: str = Field(..., description="The blockchain wallet address to analyze")

class BlockchainAnalysisTool(BaseTool):
    name: str = "Blockchain Transaction Analyzer"
    description: str = (
        "Analyzes blockchain wallet transactions using real on-chain data. "
        "Fetches transaction history, calculates volumes, detects patterns, "
        "and identifies risk indicators. Use this tool to get actual blockchain "
        "data for any Cardano wallet address."
    )
    args_schema: Type[BaseModel] = BlockchainAnalysisInput
    
    def _run(self, wallet_address: str) -> str:
        """Execute blockchain analysis"""
        try:
            # Get blockchain data
            data = get_blockchain_data(wallet_address)
            
            # Format the response for the AI agent
            result = {
                "wallet_address": wallet_address,
                "total_transactions": data["transaction_count"],
                "analysis_summary": data["analysis"],
                "preliminary_risk_score": data["risk_score"],
                "address_type": data["address_info"].get("type", "unknown"),
                "recent_transactions": data["transactions"][:5] if data["transactions"] else []
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error analyzing blockchain data: {str(e)}"


