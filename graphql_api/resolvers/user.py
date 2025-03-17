from ariadne import ObjectType, gql, make_executable_schema, SubscriptionType
from operations.user_operations import (
    get_all_users,
    get_user_by_id,
    get_user_by_username,
    get_user_by_email, 
    create_user,
    update_user,
    login
)
from schemas.User import UserCreate, UserLogin
from graphql import GraphQLError
from pydantic import ValidationError
from asyncio import Queue
from pymongo import ASCENDING, DESCENDING
from utils.token_utils import generate_reset_token
from utils.database import get_database
import json
import boto3

query = ObjectType("Query")
mutation = ObjectType("Mutation")
# subscription = SubscriptionType()

@query.field("users")
def resolve_users(*_):
    try:
        result = get_all_users()
        return {
            "users": result,
            "error": None
        }
    except Exception as e:
        print(f"Error fetching users: {e}")
        return {
            "users": [],
            "error": str(e)
        }

@query.field("user_by_id")
def resolve_get_user_by_id(obj, info, _id):
    try:
        result = get_user_by_id(_id)
        print("result", result)
        return {
            "user": result["user"] if result["user"] is not None else None,
            "error": None if result["user"] is not None else "User not found."
        }
    except Exception as e:
        print(f"Error fetching users: {e}")
        return {
            "user": None,
            "error": str(e)
        }

@query.field("user_by_username")
def resolve_get_user_by_username(obj, info, username):
    try:
        result = get_user_by_username(username)
        print("result", result)
        return {
            "user": result["user"] if result["user"] is not None else None,
            "error": None if result["user"] is not None else "User not found."
        }
    except Exception as e:
        print(f"Error fetching users: {e}")
        return {
            "user": None,
            "error": str(e)
        }

@query.field("user_by_email")
def resolve_get_user_by_email(user, info, email):
    try:
        result = get_user_by_email(email)
        return {
            "user": result["user"] if result["user"] is not None else None,
            "error": None if result["user"] is not None else "User not found."
        }
    except Exception as e:
        print(f"Error fetching users: {e}")
        return {
            "user": None,
            "error": str(e)
        }

@query.field("login")
def resolve_login(user, info, **credentials):
    user_credentials = UserLogin(**credentials)
    print("user_creds", user_credentials)
    try:
        result = login(user_credentials.model_dump())
        return {
            "success": result,
            "error": None
        }
    except Exception as e:
        print(f"Error logging in: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@mutation.field("create_user")
def resolve_create_user(_, info, **user_info):
    print("CREATE USER RESOLVER")
    try:
        user = UserCreate(**user_info)
        result = create_user(user)

        if result.get("error"):
            return {
                "user": None,
                "error": result.get("error")
            }
        
        if result.get("user"):
            return {
                "user": result.get("user"),
                "error": None
            }
        
        return {
            "user": None,
            "error": None
        }

    except ValidationError as e:
        print("ValueError e", e)
        error_msg = e.errors()[0]["msg"]
        return {
            "user": None,
            "error": error_msg
        }
    except Exception as e:
        print("Exception e", e)
        return {
            "user": None,
            "error": str(e)
        }

@mutation.field("update_user")
def resolve_update_user(_, info, **user_info):
    try:
        result = update_user(user_info)
        return {
            "user": result["user"] or {},
            "error": None
        }
    except Exception as e:
        print("Exception e", e)
        return {
            "user": None,
            "error": str(e)
        }

@mutation.field("send_reset_password_email")
async def resolve_send_reset_password_email(_, info, email):
    print("resolve_send_reset_password_email", email)

    result = get_user_by_email(email)
    user = result.get('user')
    
    if not user:
        return {
            "success": False,
            "error": "User doesn't exist."
        }
    user_id = user.get("_id")
    email = user.get("email")
    client = get_database()
    token = await generate_reset_token(user_id, email, client)
    print(token)
    print("user", user)

    return {
        "success": True,
        "error": None
    }
