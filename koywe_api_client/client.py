"""
Main Koywe API client
"""

from typing import Optional
from .auth import AuthHandler
from .endpoints import DocumentsEndpoint, AccountsEndpoint


class KoyweClient:
    """Main client for interacting with the Koywe API"""
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
        base_url: str = "https://api-billing.koywe.com/V1",
        auto_authenticate: bool = True
    ):
        """
        Initialize the Koywe API client
        
        Args:
            client_id: Your Koywe client ID
            client_secret: Your Koywe client secret
            username: Your API username
            password: Your API password
            base_url: Base URL for the API (default: production)
            auto_authenticate: Whether to authenticate immediately (default: True)
        """
        self.base_url = base_url.rstrip('/')
        
        # Initialize authentication handler
        self.auth_handler = AuthHandler(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            base_url=self.base_url
        )
        
        # Initialize endpoint handlers
        self.documents = DocumentsEndpoint(self)
        self.accounts = AccountsEndpoint(self)
        
        # Authenticate if requested
        if auto_authenticate:
            self.authenticate()
    
    def authenticate(self) -> None:
        """Authenticate with the Koywe API"""
        self.auth_handler.authenticate()
    
    def is_authenticated(self) -> bool:
        """Check if the client is currently authenticated"""
        return self.auth_handler.is_authenticated
    
    def clear_authentication(self) -> None:
        """Clear stored authentication tokens"""
        self.auth_handler.clear_tokens()
    
    @classmethod
    def from_environment(cls, auto_authenticate: bool = True) -> 'KoyweClient':
        """
        Create a client instance using environment variables
        
        Expected environment variables:
        - KOYWE_CLIENT_ID
        - KOYWE_CLIENT_SECRET
        - KOYWE_USERNAME
        - KOYWE_PASSWORD
        - KOYWE_BASE_URL (optional, defaults to production)
        
        Args:
            auto_authenticate: Whether to authenticate immediately
            
        Returns:
            KoyweClient instance
        """
        import os
        
        client_id = os.getenv('KOYWE_CLIENT_ID')
        client_secret = os.getenv('KOYWE_CLIENT_SECRET')
        username = os.getenv('KOYWE_USERNAME')
        password = os.getenv('KOYWE_PASSWORD')
        base_url = os.getenv('KOYWE_BASE_URL', 'https://api-billing.koywe.com/V1')
        
        if not all([client_id, client_secret, username, password]):
            raise ValueError(
                "Missing required environment variables. Please set: "
                "KOYWE_CLIENT_ID, KOYWE_CLIENT_SECRET, KOYWE_USERNAME, KOYWE_PASSWORD"
            )
        
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            base_url=base_url,
            auto_authenticate=auto_authenticate
        )

