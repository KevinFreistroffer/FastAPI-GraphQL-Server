from enum import Enum
from typing import Dict

class StatusCode(Enum):
    # 404 errors
    USER_NOT_FOUND = 404
    USERS_NOT_FOUND = 404
    RESOURCE_NOT_FOUND = 404
    
    # 401 errors
    INVALID_USERNAME_OR_EMAIL_AND_PASSWORD = 401
    INVALID_PASSWORD = 401
    
    # 400 errors
    INVALID_REQUEST = 400
    MISSING_PARAMETERS = 400
    
    # 422 errors
    MISSING_BODY_FIELDS = 422
    
    # 403 errors
    ACCESS_DENIED = 403
    
    # 409 errors
    USERNAME_OR_EMAIL_ALREADY_REGISTERED = 409
    USERNAME_NOT_AVAILABLE = 409
    EMAIL_NOT_AVAILABLE = 409
    
    # 500 errors
    CAUGHT_ERROR = 500
    ERROR_INSERTING_USER = 500
    COULD_NOT_UPDATE = 500
    
    # 200 success
    SUCCESS = 200

# Optional: Create error response helper
def create_error_response(status_code: StatusCode, message: str = None) -> Dict:
    """Create a standardized error response"""
    return {
        "error": message or status_code.name.lower().replace('_', ' '),
        "status_code": status_code.value
    }

# Optional: Create success response helper
def create_success_response(data: Dict = None) -> Dict:
    """Create a standardized success response"""
    response = {"status_code": StatusCode.SUCCESS.value}
    if data:
        response.update(data)
    return response