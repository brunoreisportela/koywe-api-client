"""
Account model class
"""

from typing import Dict, Any, Optional
from .base import BaseModel


class Account(BaseModel):
    """Represents an account"""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        
        # Basic account properties
        self.account_id: Optional[int] = data.get('account_id') or data.get('id')
        self.name: Optional[str] = data.get('name')
        self.tax_id: Optional[str] = data.get('tax_id')
        self.email: Optional[str] = data.get('email')
        self.phone: Optional[str] = data.get('phone')
        
        # Address information
        self.address: Optional[str] = data.get('address')
        self.city: Optional[str] = data.get('city')
        self.state: Optional[str] = data.get('state')
        self.country_id: Optional[int] = data.get('country_id')
        self.postal_code: Optional[str] = data.get('postal_code')
        
        # Business information
        self.business_type: Optional[str] = data.get('business_type')
        self.industry: Optional[str] = data.get('industry')
        
        # Status
        self.is_active: bool = data.get('is_active', True)
        self.is_verified: bool = data.get('is_verified', False)
    
    def __str__(self) -> str:
        return f"Account(id={self.account_id}, name='{self.name}')"

