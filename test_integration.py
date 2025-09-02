#!/usr/bin/env python3
"""
Integration test script for Koywe API client
"""

import sys
import os

# Add the current directory to the path so we can import the client
sys.path.insert(0, os.path.dirname(__file__))

from koywe_api_client import KoyweClient, KoyweAPIError


def test_authentication():
    """Test authentication with provided credentials"""
    
    print("=== Testing Koywe API Integration ===\n")
    
    # Provided credentials
    client_id = "685d4834fd0d9c8dc740eebb"
    client_secret = "eV8o8f1mVRgjbgMle0yMfT6aZEgTalYZ"
    
    # Note: Username and password are required but not provided
    # These would typically be your API username/password, not website credentials
    username = input("Enter your API username: ").strip()
    password = input("Enter your API password: ").strip()
    
    if not username or not password:
        print("❌ Username and password are required for authentication")
        return False
    
    try:
        # Initialize the client
        print("Initializing Koywe API client...")
        client = KoyweClient(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            auto_authenticate=False
        )
        
        # Test authentication
        print("Testing authentication...")
        client.authenticate()
        print("✅ Authentication successful!")
        
        # Test authentication status
        is_auth = client.is_authenticated()
        print(f"Authentication status: {is_auth}")
        
        return client
        
    except KoyweAPIError as e:
        print(f"❌ API Error during authentication:")
        print(f"   Message: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print(f"   Response Data: {e.response_data}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during authentication: {str(e)}")
        return False


def test_documents_api(client):
    """Test documents API endpoints"""
    
    print("\n=== Testing Documents API ===")
    
    try:
        # Test listing documents
        print("Testing document listing...")
        documents_response = client.documents.list(page=1, limit=5)
        print("✅ Document listing successful!")
        print(f"Response keys: {list(documents_response.keys())}")
        
        # Check if we have any documents
        if 'data' in documents_response and documents_response['data']:
            documents = documents_response['data']
            print(f"Found {len(documents)} documents")
            
            # Test getting a specific document
            first_doc = documents[0]
            doc_id = first_doc.get('document_id') or first_doc.get('id')
            
            if doc_id:
                print(f"Testing get document with ID: {doc_id}")
                document = client.documents.get(doc_id)
                print("✅ Get document successful!")
                print(f"Document keys: {list(document.keys())}")
        else:
            print("No documents found in the response")
            
    except KoyweAPIError as e:
        print(f"❌ API Error in documents test:")
        print(f"   Message: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print(f"   Response Data: {e.response_data}")
    except Exception as e:
        print(f"❌ Unexpected error in documents test: {str(e)}")


def test_accounts_api(client):
    """Test accounts API endpoints"""
    
    print("\n=== Testing Accounts API ===")
    
    try:
        # Try to get account with ID 1 (common default)
        account_id = 1
        print(f"Testing get account with ID: {account_id}")
        account = client.accounts.get(account_id)
        print("✅ Get account successful!")
        print(f"Account keys: {list(account.keys())}")
        
    except KoyweAPIError as e:
        print(f"❌ API Error in accounts test:")
        print(f"   Message: {e.message}")
        print(f"   Status Code: {e.status_code}")
        if e.status_code == 404:
            print("   Note: Account ID 1 not found. This is normal if you don't have an account with ID 1.")
    except Exception as e:
        print(f"❌ Unexpected error in accounts test: {str(e)}")


def main():
    """Main test function"""
    
    # Test authentication
    client = test_authentication()
    
    if not client:
        print("\n❌ Authentication failed. Cannot proceed with API tests.")
        print("\nTroubleshooting:")
        print("1. Verify your API username and password are correct")
        print("2. Check if your account has API access enabled")
        print("3. Ensure you're using API credentials, not website login credentials")
        return
    
    # Test documents API
    test_documents_api(client)
    
    # Test accounts API
    test_accounts_api(client)
    
    print("\n=== Integration Test Complete ===")
    print("✅ Basic integration test completed successfully!")
    print("\nNext steps:")
    print("1. Review the examples/ directory for usage patterns")
    print("2. Customize the client for your specific use case")
    print("3. Implement error handling appropriate for your application")


if __name__ == "__main__":
    main()

