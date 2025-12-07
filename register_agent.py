#!/usr/bin/env python3
"""
Script to register your agent with Masumi
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL", "https://masumi-payment-service-production-755f.up.railway.app/api/v1")
PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")
AGENT_IDENTIFIER = os.getenv("AGENT_IDENTIFIER")
AGENT_URL = "http://161.156.165.133.nip.io"  # Your agent's public URL
SELLER_VKEY = os.getenv("SELLER_VKEY")
NETWORK = os.getenv("NETWORK", "Preprod")

def register_agent():
    """Register the agent with Masumi"""
    
    if not PAYMENT_API_KEY:
        print("❌ Error: PAYMENT_API_KEY not set in environment")
        return False
    
    if not AGENT_IDENTIFIER:
        print("❌ Error: AGENT_IDENTIFIER not set in environment")
        return False
    
    if not SELLER_VKEY:
        print("❌ Error: SELLER_VKEY not set in environment")
        return False
    
    print("🔧 Registering agent with Masumi...")
    print(f"   Agent Identifier: {AGENT_IDENTIFIER}")
    print(f"   Agent URL: {AGENT_URL}")
    print(f"   Network: {NETWORK}")
    
    # Prepare registration data
    registration_data = {
        "agentIdentifier": AGENT_IDENTIFIER,
        "agentUrl": AGENT_URL,
        "sellerVKey": SELLER_VKEY,
        "network": NETWORK
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": PAYMENT_API_KEY
    }
    
    try:
        # Register agent endpoint
        register_url = f"{PAYMENT_SERVICE_URL}/agents/register"
        
        print(f"\n📤 Sending registration request to: {register_url}")
        response = requests.post(
            register_url,
            json=registration_data,
            headers=headers,
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Body: {response.text}")
        
        if response.status_code in [200, 201]:
            print("\n✅ Agent registered successfully!")
            print(f"   Your agent should now be visible in Masumi")
            return True
        elif response.status_code == 409:
            print("\n⚠️  Agent already registered")
            print("   Trying to update agent information...")
            
            # Try to update instead
            update_url = f"{PAYMENT_SERVICE_URL}/agents/{AGENT_IDENTIFIER}"
            update_response = requests.put(
                update_url,
                json=registration_data,
                headers=headers,
                timeout=30
            )
            
            if update_response.status_code == 200:
                print("✅ Agent information updated successfully!")
                return True
            else:
                print(f"❌ Failed to update agent: {update_response.text}")
                return False
        else:
            print(f"\n❌ Registration failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error connecting to Masumi: {str(e)}")
        return False

def verify_agent():
    """Verify the agent is accessible"""
    print("\n🔍 Verifying agent availability...")
    
    try:
        response = requests.get(f"{AGENT_URL}/availability", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent is accessible")
            print(f"   Status: {data.get('status')}")
            print(f"   Type: {data.get('type')}")
            print(f"   Agent ID: {data.get('agentIdentifier')}")
            return True
        else:
            print(f"❌ Agent not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error verifying agent: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Masumi Agent Registration")
    print("=" * 70)
    
    # First verify the agent is accessible
    if not verify_agent():
        print("\n⚠️  Warning: Agent may not be accessible from the internet")
        print("   Registration may fail if Masumi cannot reach your agent")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            exit(1)
    
    # Register the agent
    success = register_agent()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ Registration Complete!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Go to the Masumi dashboard")
        print("2. Look for your agent with identifier:")
        print(f"   {AGENT_IDENTIFIER}")
        print("3. Your agent should now be available for use")
    else:
        print("\n" + "=" * 70)
        print("❌ Registration Failed")
        print("=" * 70)
        print("\nTroubleshooting:")
        print("1. Check that PAYMENT_API_KEY is correct")
        print("2. Verify AGENT_IDENTIFIER matches your registration")
        print("3. Ensure your agent URL is publicly accessible")
        print("4. Check Masumi documentation for registration requirements")


