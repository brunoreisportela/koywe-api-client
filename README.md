# Koywe API Client

A Python client library for integrating with the Koywe e-invoicing API. This library provides a simple and intuitive interface for creating, managing, and retrieving electronic invoices across multiple markets.

## Features

- **Easy Authentication**: Automatic token management with refresh capabilities
- **Document Management**: Create, read, update, and delete invoices/documents
- **Account Management**: Manage business accounts
- **Multi-Market Support**: Works across Argentina, Chile, Colombia, Mexico, Peru, and United States
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Type Safety**: Full type hints for better development experience
- **Pagination Support**: Built-in pagination for listing operations

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from koywe_api_client import KoyweClient

# Initialize the client
client = KoyweClient(
    client_id="your_client_id",
    client_secret="your_client_secret", 
    username="your_username",
    password="your_password"
)

# Create an invoice
invoice = client.documents.create_invoice(
    issuer_info={
        "issuer_address": "123 Business St",
        "issuer_city": "Santiago",
        "issuer_phone": "+56912345678"
    },
    receiver_info={
        "receiver_address": "456 Client Ave",
        "receiver_city": "Santiago", 
        "receiver_phone": "+56987654321"
    },
    line_items=[
        {
            "product_name": "Software License",
            "quantity": 1,
            "unit_price": 1000.00,
            "total": 1000.00
        }
    ]
)

print(f"Invoice created with ID: {invoice['document_id']}")
```

## Configuration

### Using Direct Initialization

```python
client = KoyweClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_username", 
    password="your_password",
    base_url="https://api-billing.koywe.com/V1"  # Optional, defaults to production
)
```

### Using Environment Variables

Set the following environment variables:
- `KOYWE_CLIENT_ID`
- `KOYWE_CLIENT_SECRET`
- `KOYWE_USERNAME`
- `KOYWE_PASSWORD`
- `KOYWE_BASE_URL` (optional)

```python
client = KoyweClient.from_environment()
```

## API Reference

### Documents

#### List Documents
```python
# Basic listing
documents = client.documents.list(page=1, limit=10)

# With filters
documents = client.documents.list(
    page=1, 
    limit=10, 
    filters={"status": "active"}
)
```

#### Get Document
```python
document = client.documents.get(document_id=123)
```

#### Create Document
```python
# Using helper method
invoice = client.documents.create_invoice(
    issuer_info={...},
    receiver_info={...},
    line_items=[...],
    currency_id=1,
    account_id=1
)

# Using raw API
document = client.documents.create({
    "header": {...},
    "details": [...],
    "totals": {...}
})
```

#### Update Document
```python
updated_doc = client.documents.update(document_id=123, document_data={...})
```

#### Delete Document
```python
result = client.documents.delete(document_id=123)
```

### Accounts

#### Get Account
```python
account = client.accounts.get(account_id=1)
```

#### Create Account
```python
# Using helper method
account = client.accounts.create_business_account(
    business_name="My Company",
    tax_id="12345678-9",
    address="123 Business St",
    city="Santiago",
    country_id=1,
    email="contact@company.com"
)

# Using raw API
account = client.accounts.create({
    "name": "My Company",
    "tax_id": "12345678-9",
    # ... other fields
})
```

## Error Handling

The client provides specific exception types for different error scenarios:

```python
from koywe_api_client import (
    KoyweAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    NetworkError
)

try:
    client.documents.get(999999)
except NotFoundError:
    print("Document not found")
except AuthenticationError:
    print("Authentication failed")
except ValidationError as e:
    print(f"Validation error: {e.message}")
except KoyweAPIError as e:
    print(f"API error: {e.message} (Status: {e.status_code})")
```

## Examples

See the `examples/` directory for complete working examples:

- `basic_usage.py` - Basic client usage and authentication
- `create_invoice.py` - Creating invoices with different methods
- `list_documents.py` - Listing and retrieving documents

## Development

### Project Structure

```
koywe_api_client/
├── koywe_api_client/
│   ├── __init__.py
│   ├── client.py          # Main client class
│   ├── auth.py            # Authentication handler
│   ├── exceptions.py      # Custom exceptions
│   ├── endpoints/         # API endpoint handlers
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── documents.py
│   │   └── accounts.py
│   └── models/            # Data models
│       ├── __init__.py
│       ├── base.py
│       ├── document.py
│       └── account.py
├── examples/              # Usage examples
├── requirements.txt
└── README.md
```

### Running Examples

1. Update the credentials in the example files
2. Run the examples:

```bash
cd examples
python basic_usage.py
python create_invoice.py
python list_documents.py
```

## API Documentation

For complete API documentation, visit: https://docs.koywe.com/billing/introduction/👋-welcome

## Support

For issues related to this client library, please create an issue in the repository.

For API-related questions, contact Koywe support at soporte@facto.cl

## License

This project is licensed under the MIT License.

