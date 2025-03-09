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
import json
import boto3

query = ObjectType("Query")
mutation = ObjectType("Mutation")
subscription = SubscriptionType()

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

# @subscription.source("userCreated")
# async def user_created_source(obj, info):
#     print("user_created_source")
#     print("user_created_source")
#     print("user_created_source")
#     print("user_created_source")
#     print("user_created_source")
#     print("user_created_source")
#     print("user_created_source")
#     queue = Queue()
    
#     # Get MongoDB collection
#     collection = get_collection('users')
    
#     # Create change stream
#     change_stream = collection.watch(
#         [{'$match': {'operationType': 'insert'}}],
#         full_document='updateLookup'
#     )

#     try:
#         async for change in change_stream:
#             # Get the new user document
#             user_doc = change['fullDocument']
            
#             # Serialize the document
#             user = serialize_document(user_doc)
#             print("user_created_source USER", user)
#             # Remove password before sending
#             if 'password' in user:
#                 del user['password']
            
#             # Trigger Lambda function for email
#             lambda_client = boto3.client('lambda')
#             lambda_client.invoke(
#                 FunctionName='email-service-dev-hello',
#                 InvocationType='Event',
#                 Payload=json.dumps({
#                     'user': user,
#                     'email': user['email']
#                 })
#             )
            
#             # Put in queue for subscription
#             await queue.put({
#                 "user": user,
#                 "error": None
#             })
            
#     except Exception as e:
#         await queue.put({
#             "user": None,
#             "error": str(e)
#         })
    
#     return queue

# @subscription.field("userCreated")
# def user_created_resolver(event, info):
#     print("user_created_resolver")
#     print("user_created_resolver")
#     print("user_created_resolver")
#     print("user_created_resolver")
#     print("user_created_resolver")
#     return event