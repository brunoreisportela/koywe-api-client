#!/usr/bin/env python3
"""
Example of listing and retrieving documents using the Koywe API client
"""

import sys
import os

# Add the parent directory to the path so we can import the client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from koywe_api_client import KoyweClient, KoyweAPIError


def main():
    """Demonstrate listing and retrieving documents"""
    
    # Initialize the client
    client = KoyweClient(
        client_id="685d4834fd0d9c8dc740eebb",
        client_secret="eV8o8f1mVRgjbgMle0yMfT6aZEgTalYZ",
        username="your_username",  # Replace with your actual username
        password="your_password",  # Replace with your actual password
        auto_authenticate=False
    )
    
    try:
        # Authenticate
        print("Authenticating with Koywe API...")
        client.authenticate()
        print("✓ Authentication successful!")
        
        # List documents with pagination
        print("\n--- Listing documents ---")
        
        page = 1
        limit = 10
        
        documents_response = client.documents.list(page=page, limit=limit)
        print(f"Documents on page {page}:")
        print(f"Response: {documents_response}")
        
        # If there are documents, get details for the first one
        if 'data' in documents_response and documents_response['data']:
            first_doc = documents_response['data'][0]
            document_id = first_doc.get('document_id') or first_doc.get('id')
            
            if document_id:
                print(f"\n--- Getting details for document {document_id} ---")
                document_details = client.documents.get(document_id)
                print(f"Document details: {document_details}")
        
        # List documents with filters (example)
        print("\n--- Listing documents with filters ---")
        
        filters = {
            "status": "active",  # Example filter
            # Add more filters as needed based on API documentation
        }
        
        filtered_docs = client.documents.list(page=1, limit=5, filters=filters)
        print(f"Filtered documents: {filtered_docs}")
        
        # Demonstrate pagination
        print("\n--- Demonstrating pagination ---")
        
        for page_num in range(1, 4):  # Get first 3 pages
            try:
                page_docs = client.documents.list(page=page_num, limit=5)
                doc_count = len(page_docs.get('data', []))
                print(f"Page {page_num}: {doc_count} documents")
                
                if doc_count == 0:
                    print("No more documents found")
                    break
                    
            except Exception as e:
                print(f"Error fetching page {page_num}: {str(e)}")
                break
        
    except KoyweAPIError as e:
        print(f"API Error: {e.message}")
        print(f"Status Code: {e.status_code}")
        print(f"Response Data: {e.response_data}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()

