from typing import Union, Optional
from fastapi import FastAPI
from schemas.Simple import UserCreate, UserUpdate
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.database import get_collection, insert_one, find_one, find_many, update_one, serialize_document
from defs.status_codes import StatusCode, create_error_response

def get_user_with_retry(user_id, max_attempts: int = 3, delay: float = 0.5) -> Optional[dict]:
    """Try to get user multiple times with delay between attempts."""
    for attempt in range(max_attempts):
        saved_user = find_one("users", {"_id": user_id})
        if saved_user:
            return saved_user
        print(f"Attempt {attempt + 1}/{max_attempts} failed to get user {user_id}")
        time.sleep(delay)  # Wait before next attempt
    return None

def create_user(user: UserCreate):
    # Validate username is available
    existing_user = find_one('users', { 'name': user.name })

    if existing_user:
        return create_error_response(
            StatusCode.USERNAME_NOT_AVAILABLE
        )

    # Validate email is available
    existing_user = find_one('users', { 'email': user.email })
    if existing_user:
        return create_error_response(
            StatusCode.USERNAME_NOT_AVAILABLE
        )
    
    # Attempt to save to DB
    user_dict = user.model_dump()
    result = insert_one('users', user_dict)

    # Success
    # TODO: what to return to whoever is making the API request? Do they need the user object returned? 
    if result.inserted_id:
        saved_user = get_user_with_retry(result.inserted_id)
        
        if saved_user:
            return { "user": saved_user }

        # This is where logging or similar would occur so that this is known by the dev team
        # The user would need to still be able to continue onward.
        return { "error": "User created, however could not get the user from the database. Try again."}
    
    # Error
    return create_error_response(
        StatusCode.ERROR_INSERTING_USER
    )  
def get_all_users():
    users = find_many('users')
    if not users:
        return create_error_response(
            StatusCode.USERS_NOT_FOUND,
            "No users found"
        )
    return {"users": users}

def get_user_by_id(id: str):
    user = find_one('users', {"_id": id})
    if not user:
        return create_error_response(
            StatusCode.USER_NOT_FOUND,
            "User not found"
        )
    return user

def get_user_by_name(name: str):
    users = find_many('users', {"name": name})
    if not users:
        return create_error_response(
            StatusCode.USER_NOT_FOUND,
            "User not found"
        )
    return {"users": users}

def update_user(user: UserUpdate):
    result = update_one(
        'users',
        {"_id": user.id},
        user.model_dump(exclude_unset=True)
    )
    if not result.modified_count:
        return create_error_response(
            StatusCode.COULD_NOT_UPDATE,
            "User not found"
        )
    return find_one('users', {"_id": user.id})
    