#!/usr/bin/env python3
"""
Basic usage example for Koywe API client
"""

import sys
import os

# Add the parent directory to the path so we can import the client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from koywe_api_client import KoyweClient, KoyweAPIError


def main():
    """Demonstrate basic usage of the Koywe API client"""
    
    # Initialize the client with your credentials
    client = KoyweClient(
        client_id="685d4834fd0d9c8dc740eebb",
        client_secret="eV8o8f1mVRgjbgMle0yMfT6aZEgTalYZ",
        username="your_username",  # Replace with your actual username
        password="your_password",  # Replace with your actual password
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

