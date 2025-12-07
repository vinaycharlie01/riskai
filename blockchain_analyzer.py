"""
Blockchain Data Analyzer using Blockfrost API
Fetches real transaction data from Cardano blockchain
"""
import os
from typing import Dict, List, Any
from blockfrost import BlockFrostApi, ApiError
from logging_config import get_logger

logger = get_logger(__name__)

class BlockchainAnalyzer:
    """Analyzes blockchain wallet data using Blockfrost API"""
    
    def __init__(self, network: str = "preprod"):
        """
        Initialize Blockfrost API client
        
        Args:
            network: 'mainnet' or 'preprod'
        """
        self.network = network
        project_id = os.getenv("BLOCKFROST_PROJECT_ID")
    
        logger.info("🔧 INITIALIZING BLOCKCHAIN ANALYZER")
        
        if not project_id:
            logger.warning("❌ BLOCKFROST_PROJECT_ID NOT SET!")
            logger.warning("⚠️  Will use MOCK DATA for all requests")
            logger.warning("⚠️  Add BLOCKFROST_PROJECT_ID to Railway to use real data")
            self.api = None
        else:
            try:
                masked_id = project_id[:8] + "..." + project_id[-4:] if len(project_id) > 12 else "***"
                logger.info(f"✅ BLOCKFROST_PROJECT_ID found: {masked_id}")
                logger.info(f"🌐 Network: {network}")
                logger.info(f"🔗 API URL: https://cardano-{network}.blockfrost.io/api/v0")
                
                self.api = BlockFrostApi(
                    project_id=project_id,
                    base_url=f"https://cardano-{network}.blockfrost.io/api/v0"
                )
                logger.info(f"✅ BLOCKFROST API SUCCESSFULLY INITIALIZED!")
                logger.info(f"✅ Will fetch REAL blockchain data from Cardano {network}")

            except Exception as e:
                logger.error(f"❌ Failed to initialize Blockfrost: {e}")
                logger.warning("⚠️  Falling back to mock data")
                self.api = None
    
    def get_address_info(self, address: str) -> Dict[str, Any]:
        """Get basic address information"""
        if not self.api:
            logger.warning("⚠️  BLOCKFROST API NOT CONFIGURED - Using mock address info")
            return self._mock_address_info(address)
        
        try:
            logger.info(f"🔍 Fetching address info from Blockfrost for: {address}")
            info = self.api.address(address)
            result = {
                "address": address,
                "stake_address": info.stake_address,
                "type": info.type,
                "script": info.script
            }
            logger.info(f"✅ BLOCKFROST DATA RECEIVED - Address type: {info.type}, Stake: {info.stake_address}")
            return result
        except ApiError as e:
            logger.error(f"❌ Blockfrost API Error: {e}")
            logger.warning("⚠️  Falling back to mock data")
            return self._mock_address_info(address)
    
    def get_transactions(self, address: str, count: int = 100) -> List[Dict[str, Any]]:
        """Get transaction history for an address"""
        if not self.api:
            logger.warning("⚠️  BLOCKFROST API NOT CONFIGURED - Using mock transactions")
            return self._mock_transactions(address, count)
        
        try:
            logger.info(f"🔍 Fetching transactions from Blockfrost for: {address}")
            txs = self.api.address_transactions(address, count=count, order='desc')
            logger.info(f"📊 BLOCKFROST RETURNED {len(txs)} transactions")
            
            transactions = []
            for i, tx in enumerate(txs[:10]):  # Process first 10 for detailed logging
                tx_details = self.api.transaction(tx.tx_hash)
                output_amount = sum([int(out.amount[0].quantity) for out in tx_details.outputs])
                transactions.append({
                    "tx_hash": tx.tx_hash,
                    "block_height": tx.block_height,
                    "block_time": tx.block_time,
                    "output_amount": output_amount,
                    "fees": int(tx_details.fees),
                    "size": tx_details.size
                })
                
                # Log first transaction details
                if i == 0:
                    logger.info(f"✅ REAL BLOCKFROST DATA - First TX:")
                    logger.info(f"   Hash: {tx.tx_hash}")
                    logger.info(f"   Block: {tx.block_height}")
                    logger.info(f"   Amount: {output_amount / 1_000_000:.2f} ADA")
                    logger.info(f"   Fees: {int(tx_details.fees) / 1_000_000:.2f} ADA")
            
            # Process remaining transactions without detailed logging
            for tx in txs[10:]:
                tx_details = self.api.transaction(tx.tx_hash)
                transactions.append({
                    "tx_hash": tx.tx_hash,
                    "block_height": tx.block_height,
                    "block_time": tx.block_time,
                    "output_amount": sum([int(out.amount[0].quantity) for out in tx_details.outputs]),
                    "fees": int(tx_details.fees),
                    "size": tx_details.size
                })
            
            logger.info(f"✅ Successfully fetched {len(transactions)} REAL transactions from Blockfrost")
            return transactions
            
        except ApiError as e:
            logger.error(f"❌ Blockfrost API Error: {e}")
            logger.warning("⚠️  Falling back to mock data")
            return self._mock_transactions(address, count)
    
    def analyze_transaction_patterns(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze transaction patterns for risk assessment"""
        if not transactions:
            return {
                "total_transactions": 0,
                "total_volume": 0,
                "average_transaction": 0,
                "risk_indicators": []
            }
        
        total_volume = sum(tx["output_amount"] for tx in transactions)
        avg_transaction = total_volume / len(transactions) if transactions else 0
        
        # Detect suspicious patterns
        risk_indicators = []
        
        # Check for rapid transactions
        if len(transactions) > 50:
            risk_indicators.append({
                "type": "high_frequency",
                "severity": "medium",
                "description": f"High transaction frequency: {len(transactions)} transactions"
            })
        
        # Check for large transactions
        large_txs = [tx for tx in transactions if tx["output_amount"] > 100_000_000_000]  # > 100k ADA
        if large_txs:
            risk_indicators.append({
                "type": "large_transactions",
                "severity": "high",
                "description": f"Found {len(large_txs)} large transactions"
            })
        
        # Check for unusual patterns (very small or very large fees)
        avg_fee = sum(tx["fees"] for tx in transactions) / len(transactions)
        unusual_fees = [tx for tx in transactions if tx["fees"] > avg_fee * 3 or tx["fees"] < avg_fee * 0.3]
        if len(unusual_fees) > len(transactions) * 0.2:  # More than 20% unusual
            risk_indicators.append({
                "type": "unusual_fees",
                "severity": "medium",
                "description": f"Unusual fee patterns detected in {len(unusual_fees)} transactions"
            })
        
        return {
            "total_transactions": len(transactions),
            "total_volume": total_volume,
            "average_transaction": avg_transaction,
            "average_fee": avg_fee,
            "risk_indicators": risk_indicators,
            "time_span": self._calculate_time_span(transactions)
        }
    
    def calculate_risk_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate risk score based on transaction analysis"""
        base_score = 20  # Start with low risk
        
        # Add points for risk indicators
        for indicator in analysis.get("risk_indicators", []):
            if indicator["severity"] == "low":
                base_score += 5
            elif indicator["severity"] == "medium":
                base_score += 15
            elif indicator["severity"] == "high":
                base_score += 25
            elif indicator["severity"] == "critical":
                base_score += 40
        
        # Cap at 100
        return min(base_score, 100)
    
    def _calculate_time_span(self, transactions: List[Dict[str, Any]]) -> str:
        """Calculate time span of transactions"""
        if not transactions or len(transactions) < 2:
            return "N/A"
        
        oldest = min(tx["block_time"] for tx in transactions)
        newest = max(tx["block_time"] for tx in transactions)
        days = (newest - oldest) / 86400  # Convert seconds to days
        
        return f"{int(days)} days"
    
    def _mock_address_info(self, address: str) -> Dict[str, Any]:
        """Mock address info for testing"""
        return {
            "address": address,
            "stake_address": "stake_test1...",
            "type": "shelley",
            "script": False
        }
    
    def _mock_transactions(self, address: str, count: int) -> List[Dict[str, Any]]:
        """Mock transaction data for testing"""
        import time
        current_time = int(time.time())
        
        logger.warning("⚠️  USING MOCK DATA - BLOCKFROST NOT CONFIGURED!")
        
        transactions = []
        for i in range(min(count, 10)):  # Generate 10 mock transactions
            transactions.append({
                "tx_hash": f"mock_tx_{i}_{address[:8]}",
                "block_height": 1000000 + i,
                "block_time": current_time - (i * 3600),  # 1 hour apart
                "output_amount": 50_000_000 + (i * 10_000_000),  # 50-150 ADA
                "fees": 170_000 + (i * 1000),
                "size": 300 + (i * 10)
            })
        
        logger.warning(f"⚠️  Generated {len(transactions)} MOCK transactions (not real data!)")
        return transactions

def get_blockchain_data(wallet_address: str) -> Dict[str, Any]:
    """
    Main function to fetch and analyze blockchain data
    
    Args:
        wallet_address: Cardano wallet address to analyze
        
    Returns:
        Dictionary with address info, transactions, and analysis
    """
    network = os.getenv("NETWORK", "Preprod").lower()
    analyzer = BlockchainAnalyzer(network=network)
    
    # Get address info
    address_info = analyzer.get_address_info(wallet_address)
    
    # Get transactions
    transactions = analyzer.get_transactions(wallet_address, count=100)
    
    # Analyze patterns
    analysis = analyzer.analyze_transaction_patterns(transactions)
    
    # Calculate risk score
    risk_score = analyzer.calculate_risk_score(analysis)
    
    return {
        "address_info": address_info,
        "transactions": transactions,
        "analysis": analysis,
        "risk_score": risk_score,
        "transaction_count": len(transactions)
    }
