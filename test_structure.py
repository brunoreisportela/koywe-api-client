#!/usr/bin/env python3
"""
Test script to verify the package structure and imports
"""

import sys
import os

# Add the current directory to the path so we can import the client
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported correctly"""
    
    print("=== Testing Package Structure ===\n")
    
    try:
        # Test main package import
        print("Testing main package import...")
        from koywe_api_client import KoyweClient
        print("✅ KoyweClient imported successfully")
        
        # Test exception imports
        print("Testing exception imports...")
        from koywe_api_client import (
            KoyweAPIError,
            AuthenticationError,
            ValidationError,
            NotFoundError,
            RateLimitError,
            NetworkError
        )
        print("✅ All exceptions imported successfully")
        
        # Test endpoint imports
        print("Testing endpoint imports...")
        from koywe_api_client.endpoints import DocumentsEndpoint, AccountsEndpoint
        print("✅ Endpoint classes imported successfully")
        
        # Test model imports
        print("Testing model imports...")
        from koywe_api_client.models import Document, DocumentHeader, DocumentDetail, Account
        print("✅ Model classes imported successfully")
        
        # Test client initialization (without authentication)
        print("Testing client initialization...")
        client = KoyweClient(
            client_id="test_id",
            client_secret="test_secret",
            username="test_user",
            password="test_pass",
            auto_authenticate=False
        )
        print("✅ Client initialized successfully")
        
        # Test that endpoints are accessible
        print("Testing endpoint accessibility...")
        assert hasattr(client, 'documents'), "Documents endpoint not accessible"
        assert hasattr(client, 'accounts'), "Accounts endpoint not accessible"
        print("✅ All endpoints accessible")
        
        # Test authentication handler
        print("Testing authentication handler...")
        assert hasattr(client, 'auth_handler'), "Auth handler not accessible"
        assert hasattr(client.auth_handler, 'authenticate'), "Authenticate method not accessible"
        print("✅ Authentication handler accessible")
        
        print("\n✅ All structure tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


def test_client_methods():
    """Test that client methods are available"""
    
    print("\n=== Testing Client Methods ===\n")
    
    try:
        from koywe_api_client import KoyweClient
        
        client = KoyweClient(
            client_id="test_id",
            client_secret="test_secret", 
            username="test_user",
            password="test_pass",
            auto_authenticate=False
        )
        
        # Test documents methods
        print("Testing documents methods...")
        assert hasattr(client.documents, 'list'), "documents.list method missing"
        assert hasattr(client.documents, 'get'), "documents.get method missing"
        assert hasattr(client.documents, 'create'), "documents.create method missing"
        assert hasattr(client.documents, 'update'), "documents.update method missing"
        assert hasattr(client.documents, 'delete'), "documents.delete method missing"
        assert hasattr(client.documents, 'create_invoice'), "documents.create_invoice method missing"
        print("✅ All documents methods available")
        
        # Test accounts methods
        print("Testing accounts methods...")
        assert hasattr(client.accounts, 'get'), "accounts.get method missing"
        assert hasattr(client.accounts, 'create'), "accounts.create method missing"
        assert hasattr(client.accounts, 'create_business_account'), "accounts.create_business_account method missing"
        print("✅ All accounts methods available")
        
        # Test client methods
        print("Testing client methods...")
        assert hasattr(client, 'authenticate'), "authenticate method missing"
        assert hasattr(client, 'is_authenticated'), "is_authenticated method missing"
        assert hasattr(client, 'clear_authentication'), "clear_authentication method missing"
        print("✅ All client methods available")
        
        print("\n✅ All method tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing methods: {str(e)}")
        return False


def main():
    """Main test function"""
    
    print("Koywe API Client - Structure Test\n")
    
    # Test imports and structure
    structure_ok = test_imports()
    
    if not structure_ok:
        print("\n❌ Structure tests failed!")
        return
    
    # Test methods
    methods_ok = test_client_methods()
    
    if not methods_ok:
        print("\n❌ Method tests failed!")
        return
    
    print("\n" + "="*50)
    print("✅ ALL TESTS PASSED!")
    print("The Koywe API client package is properly structured.")
    print("You can now run the integration test with real credentials.")
    print("="*50)


if __name__ == "__main__":
    main()

