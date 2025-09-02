#!/usr/bin/env python3
"""
Example of creating an invoice using the Koywe API client
"""

import sys
import os
from datetime import datetime

# Add the parent directory to the path so we can import the client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from koywe_api_client import KoyweClient, KoyweAPIError


def main():
    """Demonstrate creating an invoice"""
    
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
        
        # Method 1: Create invoice using the helper method
        print("\n--- Creating invoice using helper method ---")
        
        issuer_info = {
            "issuer_address": "123 Business Street",
            "issuer_city": "Santiago",
            "issuer_district": "Las Condes",
            "issuer_phone": "+56912345678",
            "issuer_activity": "Software Development"
        }
        
        receiver_info = {
            "receiver_address": "456 Client Avenue", 
            "receiver_city": "Santiago",
            "receiver_district": "Providencia",
            "receiver_phone": "+56987654321",
            "receiver_activity": "Retail"
        }
        
        line_items = [
            {
                "product_name": "Software License",
                "description": "Annual software license",
                "quantity": 1,
                "unit_price": 1000.00,
                "total": 1000.00
            },
            {
                "product_name": "Support Services",
                "description": "Technical support for 12 months",
                "quantity": 12,
                "unit_price": 50.00,
                "total": 600.00
            }
        ]
        
        invoice = client.documents.create_invoice(
            issuer_info=issuer_info,
            receiver_info=receiver_info,
            line_items=line_items,
            currency_id=1,  # Adjust based on your needs
            account_id=1    # Adjust based on your account
        )
        
        print(f"✓ Invoice created successfully!")
        print(f"Document ID: {invoice.get('document_id')}")
        print(f"Invoice data: {invoice}")
        
        # Method 2: Create document using raw API call
        print("\n--- Creating document using raw API call ---")
        
        document_data = {
            "header": {
                "document_type_id": 1,
                "issue_date": datetime.now().strftime("%Y-%m-%d"),
                "currency_id": 1,
                "account_id": 1,
                "issuer_address": "789 Company Blvd",
                "issuer_city": "Santiago",
                "receiver_address": "321 Customer St",
                "receiver_city": "Santiago"
            },
            "details": [
                {
                    "product_name": "Consulting Services",
                    "quantity": 10,
                    "unit_price": 150.00,
                    "total": 1500.00
                }
            ],
            "totals": {
                "subtotal": 1500.00,
                "tax": 150.00,
                "total": 1650.00
            }
        }
        
        document = client.documents.create(document_data)
        print(f"✓ Document created successfully!")
        print(f"Document ID: {document.get('document_id')}")
        
    except KoyweAPIError as e:
        print(f"API Error: {e.message}")
        print(f"Status Code: {e.status_code}")
        print(f"Response Data: {e.response_data}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()

