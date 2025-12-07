"""
RiskLens AI Crew
Orchestrates multiple agents for blockchain risk analysis
"""
from crewai import Crew, Task
from agents import TransactionAnalyzerAgent, RiskScorerAgent, ComplianceReporterAgent
from core.logging import get_logger

logger = get_logger(__name__)

class RiskAnalysisCrew:
    """
    RiskLens AI - Blockchain Compliance & Risk Scoring Agent
    Analyzes wallet transactions and provides risk assessment
    """
    
    def __init__(self, verbose: bool = True, logger_instance=None):
        """Initialize the crew with specialized agents"""
        self.verbose = verbose
        self.logger = logger_instance or logger
        self.crew = self._create_crew()
        self.logger.info("RiskAnalysisCrew initialized for blockchain compliance analysis")
    
    def _create_crew(self) -> Crew:
        """Create the crew with agents and tasks"""
        self.logger.info("Creating RiskLens AI crew with specialized agents")
        
        # Create agents
        transaction_analyzer = TransactionAnalyzerAgent.create(self.verbose)
        risk_scorer = RiskScorerAgent.create(self.verbose)
        compliance_reporter = ComplianceReporterAgent.create(self.verbose)
        
        self.logger.info("Created specialized risk analysis agents")
        
        # Define tasks
        tasks = [
            Task(
                description="""Analyze the wallet address: {wallet_address}
                
                Examine all available transaction data and identify:
                1. Transaction patterns and frequency
                2. Unusual or suspicious activities
                3. Connections to known risky addresses
                4. Use of mixers or privacy tools
                5. Large or rapid fund movements
                6. Interaction with DeFi protocols
                7. Any red flags or anomalies
                
                Provide a detailed analysis of findings.""",
                expected_output="""Detailed transaction analysis report including:
                - Transaction pattern summary
                - List of suspicious activities found
                - Connections to risky entities
                - Behavioral patterns identified
                - Key risk indicators""",
                agent=transaction_analyzer
            ),
            Task(
                description="""Based on the transaction analysis, calculate a comprehensive risk score.
                
                Consider these factors:
                - Transaction patterns (frequency, amounts, timing)
                - Suspicious activity indicators
                - Connections to known scams or mixers
                - Compliance with normal behavior patterns
                - Historical wallet behavior
                
                Assign a risk score from 0-100 and categorize as:
                - 0-20: Low Risk (Green)
                - 21-50: Medium Risk (Yellow)
                - 51-75: High Risk (Orange)
                - 76-100: Critical Risk (Red)
                
                Explain the reasoning behind the score.""",
                expected_output="""Risk assessment including:
                - Overall risk score (0-100)
                - Risk category (Low/Medium/High/Critical)
                - Breakdown of risk factors
                - Confidence level in assessment
                - Key risk contributors""",
                agent=risk_scorer
            ),
            Task(
                description="""Generate a comprehensive compliance report for wallet: {wallet_address}
                
                Create a professional report that includes:
                1. Executive Summary
                2. Wallet Overview
                3. Transaction Analysis Findings
                4. Risk Score and Category
                5. Detailed Risk Factors
                6. Suspicious Activity Details
                7. Recommendations
                8. Compliance Status
                
                Make it clear, actionable, and suitable for:
                - Regulatory review
                - Exchange KYC/AML processes
                - User understanding
                - On-chain publication
                
                Use simple language that anyone can understand.""",
                expected_output="""Complete compliance report in JSON format with:
                {
                    "wallet_address": "address",
                    "analysis_timestamp": "ISO timestamp",
                    "risk_score": 0-100,
                    "risk_category": "Low/Medium/High/Critical",
                    "trust_score": 0-100,
                    "executive_summary": "brief overview",
                    "transaction_summary": {
                        "total_transactions": number,
                        "total_volume": "amount",
                        "active_period": "duration",
                        "counterparties": number
                    },
                    "risk_factors": [
                        {
                            "factor": "name",
                            "severity": "Low/Medium/High/Critical",
                            "description": "explanation",
                            "impact": "how it affects score"
                        }
                    ],
                    "suspicious_activities": [
                        {
                            "activity": "description",
                            "severity": "level",
                            "evidence": "details"
                        }
                    ],
                    "recommendations": [
                        "action items"
                    ],
                    "compliance_status": "Compliant/Non-Compliant/Requires Review",
                    "confidence_level": "High/Medium/Low",
                    "report_hash": "for on-chain verification"
                }""",
                agent=compliance_reporter
            )
        ]
        
        # Create crew
        crew = Crew(
            agents=[transaction_analyzer, risk_scorer, compliance_reporter],
            tasks=tasks
        )
        
        self.logger.info("RiskLens AI crew setup completed")
        return crew

