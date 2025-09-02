"""
Documents endpoint for managing invoices and documents
"""

from typing import Dict, Any, Optional, List
from .base import BaseEndpoint


class DocumentsEndpoint(BaseEndpoint):
    """Handles document/invoice operations"""
    
    def list(
        self, 
        page: int = 1, 
        limit: int = 10, 
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get a paginated list of documents
        
        Args:
            page: Page number (default: 1)
            limit: Number of items per page (default: 10)
            filters: Additional filters to apply
            
        Returns:
            Dict containing documents list and pagination info
        """
        params = {
            "page": page,
            "limit": limit
        }
        
        if filters:
            params.update(filters)
        
        return self.get("documents", params=params)
    
    def get(self, document_id: int) -> Dict[str, Any]:
        """
        Get a specific document by ID
        
        Args:
            document_id: The document ID
            
        Returns:
            Dict containing document details
        """
        return super().get(f"documents/{document_id}")
    
    def create(
        self, 
        document_data: Dict[str, Any], 
        generate_stamp: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a new document/invoice
        
        Args:
            document_data: Document data including header, details, totals, etc.
            generate_stamp: Optional parameter to generate stamp
            
        Returns:
            Dict containing created document details
        """
        endpoint = "documents"
        if generate_stamp is not None:
            endpoint += f"?generate_stamp={generate_stamp}"
        
        return self.post(endpoint, data=document_data)
    
    def update(self, document_id: int, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a specific document
        
        Args:
            document_id: The document ID
            document_data: Updated document data
            
        Returns:
            Dict containing updated document details
        """
        return self.put(f"documents/{document_id}", data=document_data)
    
    def delete(self, document_id: int) -> Dict[str, Any]:
        """
        Delete a specific document
        
        Args:
            document_id: The document ID
            
        Returns:
            Dict containing deletion confirmation
        """
        return super().delete(f"documents/{document_id}")
    
    def create_invoice(
        self,
        issuer_info: Dict[str, Any],
        receiver_info: Dict[str, Any],
        line_items: List[Dict[str, Any]],
        currency_id: int = 1,
        document_type_id: int = 1,
        account_id: int = 1,
        additional_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Helper method to create a standard invoice
        
        Args:
            issuer_info: Issuer information (address, tax_id, etc.)
            receiver_info: Receiver information (address, tax_id, etc.)
            line_items: List of invoice line items
            currency_id: Currency ID (default: 1)
            document_type_id: Document type ID (default: 1)
            account_id: Account ID (default: 1)
            additional_options: Additional options for the invoice
            
        Returns:
            Dict containing created invoice details
        """
        
        # Calculate totals
        subtotal = sum(item.get('total', 0) for item in line_items)
        tax_rate = 0.1  # Default 10% tax, should be configurable
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount
        
        # Build document structure
        document_data = {
            "header": {
                "document_type_id": document_type_id,
                "issue_date": self._get_current_date(),
                "currency_id": currency_id,
                "account_id": account_id,
                **issuer_info,
                **receiver_info
            },
            "details": line_items,
            "totals": {
                "subtotal": subtotal,
                "tax": tax_amount,
                "total": total
            }
        }
        
        # Add additional options if provided
        if additional_options:
            document_data.update(additional_options)
        
        return self.create(document_data)
    
    def _get_current_date(self) -> str:
        """Get current date in YYYY-MM-DD format"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

