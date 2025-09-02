"""
Authentication handler for Koywe API
"""

import time
from typing import Optional, Dict, Any
import requests
from .exceptions import AuthenticationError, NetworkError


class AuthHandler:
    """Handles authentication with the Koywe API"""
    
    def __init__(self, client_id: str, client_secret: str, username: str, password: str, base_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip('/')
        
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expires_at: Optional[float] = None
        self._token_type: str = "Bearer"
    
    @property
    def is_authenticated(self) -> bool:
        """Check if we have a valid access token"""
        return (
            self._access_token is not None and
            self._token_expires_at is not None and
            time.time() < self._token_expires_at
        )
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authorization headers for API requests"""
        if not self.is_authenticated:
            self.authenticate()
        
        return {
            "Authorization": f"{self._token_type} {self._access_token}"
        }
    
    def authenticate(self) -> None:
        """Authenticate with the Koywe API and obtain access token"""
        auth_url = f"{self.base_url}/auth"
        
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(auth_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self._process_auth_response(data)
            elif response.status_code == 401:
                raise AuthenticationError(
                    "Invalid credentials provided",
                    status_code=response.status_code,
                    response_data=response.json() if response.content else {}
                )
            else:
                raise AuthenticationError(
                    f"Authentication failed with status {response.status_code}",
                    status_code=response.status_code,
                    response_data=response.json() if response.content else {}
                )
                
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error during authentication: {str(e)}")
    
    def _process_auth_response(self, data: Dict[str, Any]) -> None:
        """Process the authentication response and store tokens"""
        self._access_token = data.get("access_token")
        self._refresh_token = data.get("refresh_token")
        self._token_type = data.get("token_type", "Bearer")
        
        # Calculate expiration time
        expires_in = data.get("expires_in", 3600)  # Default to 1 hour
        self._token_expires_at = time.time() + expires_in - 60  # Refresh 1 minute early
        
        if not self._access_token:
            raise AuthenticationError("No access token received from authentication response")
    
    def refresh_access_token(self) -> None:
        """Refresh the access token using the refresh token"""
        if not self._refresh_token:
            # If no refresh token, re-authenticate
            self.authenticate()
            return
        
        auth_url = f"{self.base_url}/auth"
        
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(auth_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self._process_auth_response(data)
            else:
                # If refresh fails, try full authentication
                self.authenticate()
                
        except requests.exceptions.RequestException:
            # If refresh fails, try full authentication
            self.authenticate()
    
    def clear_tokens(self) -> None:
        """Clear stored authentication tokens"""
        self._access_token = None
        self._refresh_token = None
        self._token_expires_at = None

