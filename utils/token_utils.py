import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import os
import jwt
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

# Constants
TOKEN_EXPIRY_HOURS = 24
JWT_SECRET = os.getenv('JWT_SECRET', secrets.token_urlsafe(32))

async def generate_reset_token(user_id: str, email: str, client: AsyncIOMotorClient) -> Dict[str, str]:
    """
    Generate a password reset token and store it in the database.
    
    Args:
        user_id: The user's ID
        email: The user's email
        client: MongoDB client
    
    Returns:
        Dict containing the token and expiry
    """
    try:
        # Generate token payload
        expiry = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
        
        # Create JWT token
        token_payload = {
            'user_id': str(user_id),
            'email': email,
            'type': 'password_reset',
            'exp': expiry
        }
        
        token = jwt.encode(token_payload, JWT_SECRET, algorithm='HS256')
        
        # Store token in database
        await client.journal.password_reset_tokens.insert_one({
            'user_id': ObjectId(user_id),
            'token': token,
            'email': email,
            'expiry': expiry,
            'used': False,
            'created_at': datetime.utcnow()
        })
        
        return {
            'token': token,
            'expiry': expiry.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating reset token: {e}")
        raise

async def verify_reset_token(token: str, client: AsyncIOMotorClient) -> Optional[Dict]:
    """
    Verify a password reset token.
    
    Args:
        token: The reset token
        client: MongoDB client
    
    Returns:
        Dict containing user info if valid, None if invalid
    """
    try:
        # Verify JWT
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
            
        # Check token in database
        token_doc = await client.journal.password_reset_tokens.find_one({
            'token': token,
            'used': False,
            'expiry': {'$gt': datetime.utcnow()}
        })
        
        if not token_doc:
            logger.warning("Token not found or already used")
            return None
            
        return {
            'user_id': payload['user_id'],
            'email': payload['email']
        }
        
    except Exception as e:
        logger.error(f"Error verifying reset token: {e}")
        return None

async def invalidate_reset_token(token: str, client: AsyncIOMotorClient) -> bool:
    """
    Mark a reset token as used.
    
    Args:
        token: The reset token
        client: MongoDB client
    
    Returns:
        bool: True if token was invalidated, False otherwise
    """
    try:
        result = await client.journal.password_reset_tokens.update_one(
            {'token': token},
            {'$set': {'used': True}}
        )
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error invalidating reset token: {e}")
        return False

async def cleanup_expired_tokens(client: AsyncIOMotorClient) -> int:
    """
    Remove expired tokens from database.
    
    Args:
        client: MongoDB client
    
    Returns:
        int: Number of tokens removed
    """
    try:
        result = await client.journal.password_reset_tokens.delete_many({
            'expiry': {'$lt': datetime.utcnow()}
        })
        return result.deleted_count
    except Exception as e:
        logger.error(f"Error cleaning up tokens: {e}")
        return 0 