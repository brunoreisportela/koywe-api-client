"""
Accounts endpoint for managing account operations
"""

from typing import Dict, Any, Optional
from .base import BaseEndpoint


class AccountsEndpoint(BaseEndpoint):
    """Handles account operations"""
    
    def get(self, account_id: int) -> Dict[str, Any]:
        """
        Get a specific account by ID
        
        Args:
            account_id: The account ID
            
        Returns:
            Dict containing account details
        """
        return super().get(f"accounts/{account_id}")
    
    def create(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new account
        
        Args:
            account_data: Account data including name, address, tax info, etc.
            
        Returns:
            Dict containing created account details
        """
        return self.post("accounts", data=account_data)
    
    def create_business_account(
        self,
        business_name: str,
        tax_id: str,
        address: str,
        city: str,
        country_id: int,
        email: str,
        phone: Optional[str] = None,
        additional_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Helper method to create a business account
        
        Args:
            business_name: Name of the business
            tax_id: Tax identification number
            address: Business address
            city: City
            country_id: Country ID
            email: Contact email
            phone: Contact phone (optional)
            additional_info: Additional account information
            
        Returns:
            Dict containing created account details
        """
        
        account_data = {
            "name": business_name,
            "tax_id": tax_id,
            "address": address,
            "city": city,
            "country_id": country_id,
            "email": email
        }
        
        if phone:
            account_data["phone"] = phone
        
        if additional_info:
            account_data.update(additional_info)
        
        return self.create(account_data)

