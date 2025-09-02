"""
Base model class for all Koywe API objects
"""

from typing import Dict, Any, Optional
from datetime import datetime


class BaseModel:
    """Base class for all API models"""
    
    def __init__(self, data: Dict[str, Any]):
        self._data = data
        self._parse_data()
    
    def _parse_data(self) -> None:
        """Parse the raw data into model attributes"""
        for key, value in self._data.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model back to a dictionary"""
        return self._data.copy()
    
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({self._data})"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    @staticmethod
    def _parse_datetime(date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string into a datetime object"""
        if not date_str:
            return None
        
        # Try different date formats
        formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None

