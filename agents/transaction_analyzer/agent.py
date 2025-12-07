"""
Transaction Analyzer Agent
Analyzes blockchain transactions and identifies patterns
"""
from crewai import Agent
from services.blockchain.tools import BlockchainAnalysisTool

class TransactionAnalyzerAgent:
    """Creates and configures the Transaction Analyzer agent"""
    
    @staticmethod
    def create(verbose: bool = True) -> Agent:
        """Create Transaction Analyzer agent"""
        return Agent(
            role='Blockchain Transaction Analyzer',
            goal='Analyze wallet transactions and identify patterns, anomalies, and suspicious activities',
            backstory="""You are an expert blockchain forensics analyst with deep knowledge of
            transaction patterns, money laundering techniques, and blockchain security. You can
            identify suspicious patterns like mixer usage, rapid transfers, unusual amounts,
            connections to known scam addresses, and other red flags in wallet activity.""",
            tools=[BlockchainAnalysisTool()],
            verbose=verbose
        )

