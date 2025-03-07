from typing import Union
from fastapi import FastAPI
from schemas.Simple import UserCreate, UserUpdate
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.database import get_collection, insert_one, find_one, find_many, update_one, serialize_document

def create_new_user(user: UserCreate):
    user_dict = user.model_dump()
    result = insert_one('users', user_dict)
    return {"id": str(result.inserted_id)}

def get_all_users():
    users = find_many('users')
    return {"users": users}

def get_user_by_id(id: str):
    user = find_one('users', {"_id": id})
    if not user:
        return {"error": "User not found"}
    return user

def get_user_by_name(name: str):
    users = find_many('users', {"name": name})
    if not users:
        return {"error": "User not found"}
    return {"users": users}

def update_user(user: UserUpdate):
    result = update_one(
        'users',
        {"_id": user.id},
        user.model_dump(exclude_unset=True)
    )
    if result.modified_count:
        return find_one('users', {"_id": user.id})
    return {"error": "User not found"}
    