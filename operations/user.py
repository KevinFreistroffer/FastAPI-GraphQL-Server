from typing import Union
from fastapi import FastAPI
from schemas.Simple import UserCreate, UserUpdate
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.database import get_collection, insert_one, find_one, find_many, update_one, serialize_document

def create_new_user(user: UserCreate):
    try:
        user_dict = user.model_dump()
        result = insert_one('users', user_dict)
        return {"id": str(result.inserted_id)}
    except Exception as e:
        print(f"Error creating user: {e}")
        return {"error": str(e)}

def get_all_users():
    try:
        users = find_many('users')
        return {"users": users}
    except Exception as e:
        print(f"Error getting users: {e}")
        return {"users": []}

def get_user_by_id(id: str):
    try:
        user = find_one('users', {"_id": id})
        return user if user else {"error": "User not found"}
    except Exception as e:
        print(f"Error getting user: {e}")
        return {"error": str(e)}

def get_user_by_name(name: str):
    try:
        # MongoDB query using the name field
        users = find_many('users', {"name": name})
        
        if not users:
            return {"error": "User not found"}
        
        return {
            "users": users  # Already serialized by find_many
        }
    except Exception as e:
        print(f"Error finding users: {e}")
        return {"error": f"An error occurred: {e}"}

def update_user(user: UserUpdate):
    try:
        result = update_one(
            'users',
            {"_id": user.id},
            user.model_dump(exclude_unset=True)
        )
        if result.modified_count:
            return find_one('users', {"_id": user.id})
        return {"error": "User not found"}
    except Exception as e:
        print(f"Error updating user: {e}")
        return {"error": str(e)}
    