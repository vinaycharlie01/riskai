"""
Result Formatters
Format analysis results for different outputs
"""
from typing import Dict, Any

def format_result_for_display(result_dict: Dict[str, Any]) -> str:
    """
    Format the JSON result as a nicely formatted string for Sokosumi dashboard.
    The dashboard only accepts plain strings, not JSON objects.
    """
    if not isinstance(result_dict, dict):
        return str(result_dict)
    
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

