#!/usr/bin/env python3
"""
Basic usage example for Koywe API client
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to the path so we can import the client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from koywe_api_client import KoyweClient, KoyweAPIError


def main():
    """Demonstrate basic usage of the Koywe API client"""
    
    # Load credentials from environment variables
    client_id = os.getenv("KOYWE_CLIENT_ID")
    client_secret = os.getenv("KOYWE_CLIENT_SECRET")
    username = os.getenv("KOYWE_USERNAME", "your_username")  # Default fallback
    password = os.getenv("KOYWE_PASSWORD", "your_password")  # Default fallback
    
    if not client_id or not client_secret:
        print("❌ Missing credentials in environment variables")
        print("Please ensure KOYWE_CLIENT_ID and KOYWE_CLIENT_SECRET are set in your .env file")
        return
    
    # Initialize the client with your credentials
    client = KoyweClient(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        auto_authenticate=False  # Don't authenticate immediately for this example
    )
    
    try:
        # Authenticate
        print("Authenticating with Koywe API...")
        client.authenticate()
        print("✓ Authentication successful!")
        
        # Check authentication status
        print(f"Is authenticated: {client.is_authenticated()}")
        
        # List documents
        print("\nFetching documents...")
        documents_response = client.documents.list(page=1, limit=5)
        print(f"Documents response: {documents_response}")
        
        # Get account information (if you have an account ID)
        # account_id = 1  # Replace with actual account ID
        # print(f"\nFetching account {account_id}...")
        # account = client.accounts.get(account_id)
        # print(f"Account: {account}")
        
    except KoyweAPIError as e:
        print(f"API Error: {e.message}")
        print(f"Status Code: {e.status_code}")
        print(f"Response Data: {e.response_data}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()

