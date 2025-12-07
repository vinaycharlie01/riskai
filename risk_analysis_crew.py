from crewai import Agent, Crew, Task
from logging_config import get_logger
from blockchain_tools import BlockchainAnalysisTool
import json

class RiskAnalysisCrew:
    """
    RiskLens AI - Blockchain Compliance & Risk Scoring Agent
    Analyzes wallet transactions and provides risk assessment
    """
    
    def __init__(self, verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()
        self.logger.info("RiskAnalysisCrew initialized for blockchain compliance analysis")

    def create_crew(self):
        self.logger.info("Creating RiskLens AI crew with specialized agents")
        
        # Initialize blockchain analysis tool
        blockchain_tool = BlockchainAnalysisTool()
        
        # Agent 1: Transaction Analyzer
        transaction_analyzer = Agent(
            role='Blockchain Transaction Analyzer',
            goal='Analyze wallet transactions and identify patterns, anomalies, and suspicious activities',
            backstory="""You are an expert blockchain forensics analyst with deep knowledge of
            transaction patterns, money laundering techniques, and blockchain security. You can
            identify suspicious patterns like mixer usage, rapid transfers, unusual amounts,
            connections to known scam addresses, and other red flags in wallet activity.""",
            tools=[blockchain_tool],
            verbose=self.verbose
        )

        # Agent 2: Risk Scorer
        risk_scorer = Agent(
            role='Risk Assessment Specialist',
            goal='Calculate comprehensive risk scores based on transaction analysis and behavioral patterns',
            backstory="""You are a risk assessment expert specializing in financial compliance 
            and AML (Anti-Money Laundering) regulations. You evaluate transaction patterns, 
            wallet behavior, and connections to assign accurate risk scores from 0-100, where 
            0 is completely safe and 100 is extremely high risk. You consider factors like 
            transaction frequency, amounts, counterparty risk, and regulatory compliance.""",
            verbose=self.verbose
        )

        # Agent 3: Compliance Report Generator
        compliance_reporter = Agent(
            role='Compliance Report Specialist',
            goal='Generate clear, detailed compliance reports with actionable insights',
            backstory="""You are a compliance documentation expert who creates professional, 
            easy-to-understand reports for regulators, exchanges, and users. You explain 
            complex risk factors in simple terms, provide clear recommendations, and ensure 
            all findings are well-documented and verifiable. Your reports meet international 
            compliance standards and are suitable for on-chain publication.""",
            verbose=self.verbose
        )

        self.logger.info("Created specialized risk analysis agents")

        # Define the analysis workflow
        crew = Crew(
            agents=[transaction_analyzer, risk_scorer, compliance_reporter],
            tasks=[
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
        )
        
        self.logger.info("RiskLens AI crew setup completed")
        return crew


