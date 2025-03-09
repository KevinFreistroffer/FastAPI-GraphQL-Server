from ariadne import ObjectType, gql, make_executable_schema
from operations.user_operations import get_all_users, create_user, get_user_by_username, get_user_by_email, update_user
from schemas.User import UserCreate
from graphql import GraphQLError
from pydantic import ValidationError

query = ObjectType("Query")
mutation = ObjectType("Mutation")

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


@mutation.field("create_user")
def resolve_create_user(_, info, **user_info):
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
        result = update_user(**user_info)
        print(result)

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