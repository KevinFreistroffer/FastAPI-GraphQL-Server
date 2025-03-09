from typing import Union, Optional
from fastapi import FastAPI
from schemas.User import UserCreate, UserUpdate
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.database import get_collection, insert_one, find_one, find_many, update_one, serialize_document
from utils.hash import hash_password
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
    user_dict["password"] = hash_password(user_dict["password"])
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
    return users

def get_user_by_id(_id: str):
    result = find_one('users', {"_id": _id})
    print(result)
    print(result)
    print(result)
    print(result)
    print(result)
    return {"user": result}

def get_user_by_name(name: str):
    result = find_one('users', {"name": name})
    return {"user": result}

def get_user_by_email(email: str):
    result = find_one('users', {"email": email})
    return {"user": result}

def get_user_by_username(username: str):
    result = find_one('users', {"username": username})
    return {"user": result}

def update_user(user_data: dict):
    print("db op update_user()", user_data)
    user = UserUpdate(**user_data)
    
    result = update_one(
        'users',
        {"_id": user.id},
        user.model_dump(exclude_unset=True, exclude={"id"})
    )
    
    # Print the UpdateResult details
    print(f"Result details:")
    print(f"- Matched count: {result.matched_count}")
    print(f"- Modified count: {result.modified_count}")
    
    # Check if update was successful
    if not result.modified_count:
        return {
            "user": None,
            "error": "User not found"
        }
    
    # Get the updated user
    updated_user = find_one('users', {"_id": user.id})
    print("updated_user", updated_user)
    return {
        "user": updated_user,
        "error": None
    }
    