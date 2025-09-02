"""
Base endpoint class with common functionality
"""

from typing import Dict, Any, Optional, List, Union
import requests
from ..exceptions import (
    KoyweAPIError, 
    AuthenticationError, 
    ValidationError, 
    NotFoundError, 
    RateLimitError, 
    NetworkError,
    ServerError
)


class BaseEndpoint:
    """Base class for all API endpoints"""
    
    def __init__(self, client):
        self.client = client
        self.base_url = client.base_url
        self.auth_handler = client.auth_handler
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make an authenticated HTTP request to the API"""
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Get authentication headers
        auth_headers = self.auth_handler.get_auth_headers()
        
        # Merge headers
        request_headers = {
            "Content-Type": "application/json",
            **auth_headers
        }
        if headers:
            request_headers.update(headers)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=request_headers,
                timeout=30
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            raise NetworkError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Connection error occurred")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions"""
        
        try:
            response_data = response.json() if response.content else {}
        except ValueError:
            response_data = {}
        
        if response.status_code == 200 or response.status_code == 201:
            return response_data
        elif response.status_code == 400:
            raise ValidationError(
                "Bad request - validation failed",
                status_code=response.status_code,
                response_data=response_data
            )
        elif response.status_code == 401:
            # Try to refresh token and retry once
            self.auth_handler.clear_tokens()
            raise AuthenticationError(
                "Authentication failed",
                status_code=response.status_code,
                response_data=response_data
            )
        elif response.status_code == 404:
            raise NotFoundError(
                "Resource not found",
                status_code=response.status_code,
                response_data=response_data
            )
        elif response.status_code == 429:
            raise RateLimitError(
                "Rate limit exceeded",
                status_code=response.status_code,
                response_data=response_data
            )
        elif 500 <= response.status_code < 600:
            raise ServerError(
                f"Server error: {response.status_code}",
                status_code=response.status_code,
                response_data=response_data
            )
        else:
            raise KoyweAPIError(
                f"Unexpected error: {response.status_code}",
                status_code=response.status_code,
                response_data=response_data
            )
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request"""
        return self._make_request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request"""
        return self._make_request("POST", endpoint, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request"""
        return self._make_request("PUT", endpoint, data=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request"""
        return self._make_request("DELETE", endpoint)

