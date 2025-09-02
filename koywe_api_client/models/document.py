"""
Document model classes
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import BaseModel


class DocumentDetail(BaseModel):
    """Represents a document line item/detail"""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        
        # Common properties
        self.product_name: Optional[str] = data.get('product_name')
        self.quantity: Optional[float] = data.get('quantity')
        self.unit_price: Optional[float] = data.get('unit_price')
        self.total: Optional[float] = data.get('total')
        self.description: Optional[str] = data.get('description')


class DocumentHeader(BaseModel):
    """Represents document header information"""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        
        # Common header properties
        self.document_type_id: Optional[int] = data.get('document_type_id')
        self.issue_date: Optional[datetime] = self._parse_datetime(data.get('issue_date'))
        self.currency_id: Optional[int] = data.get('currency_id')
        self.account_id: Optional[int] = data.get('account_id')
        
        # Issuer information
        self.issuer_address: Optional[str] = data.get('issuer_address')
        self.issuer_city: Optional[str] = data.get('issuer_city')
        self.issuer_district: Optional[str] = data.get('issuer_district')
        self.issuer_phone: Optional[str] = data.get('issuer_phone')
        self.issuer_activity: Optional[str] = data.get('issuer_activity')
        
        # Receiver information
        self.receiver_address: Optional[str] = data.get('receiver_address')
        self.receiver_city: Optional[str] = data.get('receiver_city')
        self.receiver_district: Optional[str] = data.get('receiver_district')
        self.receiver_phone: Optional[str] = data.get('receiver_phone')
        self.receiver_activity: Optional[str] = data.get('receiver_activity')


class Document(BaseModel):
    """Represents a complete document/invoice"""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        
        # Basic properties
        self.document_id: Optional[int] = data.get('document_id')
        
        # Parse header
        header_data = data.get('header', {})
        self.header: DocumentHeader = DocumentHeader(header_data)
        
        # Parse details
        details_data = data.get('details', [])
        self.details: List[DocumentDetail] = [
            DocumentDetail(detail) for detail in details_data
        ]
        
        # Parse totals
        totals_data = data.get('totals', {})
        self.subtotal: Optional[float] = totals_data.get('subtotal')
        self.tax: Optional[float] = totals_data.get('tax')
        self.total: Optional[float] = totals_data.get('total')
        
        # Electronic document info
        electronic_doc = data.get('electronic_document', {})
        self.electronic_document_id: Optional[str] = electronic_doc.get('id')
        self.electronic_document_url: Optional[str] = electronic_doc.get('url')
        
        # Payment link
        payment_link = data.get('payment_link', {})
        self.payment_link_url: Optional[str] = payment_link.get('url')
    
    @property
    def is_electronic(self) -> bool:
        """Check if this is an electronic document"""
        return self.electronic_document_id is not None
    
    @property
    def has_payment_link(self) -> bool:
        """Check if this document has a payment link"""
        return self.payment_link_url is not None
    
    def get_line_items_total(self) -> float:
        """Calculate total from line items"""
        return sum(detail.total or 0 for detail in self.details)
    
    def __str__(self) -> str:
        return f"Document(id={self.document_id}, total={self.total})"

