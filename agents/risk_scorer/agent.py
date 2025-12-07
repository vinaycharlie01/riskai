"""
Risk Scorer Agent
Calculates comprehensive risk scores based on transaction analysis
"""
from crewai import Agent

class RiskScorerAgent:
    """Creates and configures the Risk Scorer agent"""
    
    @staticmethod
    def create(verbose: bool = True) -> Agent:
        """Create Risk Scorer agent"""
        return Agent(
            role='Risk Assessment Specialist',
            goal='Calculate comprehensive risk scores based on transaction analysis and behavioral patterns',
            backstory="""You are a risk assessment expert specializing in financial compliance 
            and AML (Anti-Money Laundering) regulations. You evaluate transaction patterns, 
            wallet behavior, and connections to assign accurate risk scores from 0-100, where 
            0 is completely safe and 100 is extremely high risk. You consider factors like 
            transaction frequency, amounts, counterparty risk, and regulatory compliance.""",
            verbose=verbose
        )

