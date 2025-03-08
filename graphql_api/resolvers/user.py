from ariadne import ObjectType, gql, make_executable_schema
from operations.user_operations import get_all_users
from operations.user_operations import create_user
from schemas.User import UserCreate
from graphql import GraphQLError
from pydantic import ValidationError

query = ObjectType("Query")
mutation = ObjectType("Mutation")

@query.field("users")
def resolve_users(*_):
    try:
        result = get_all_users()
        if not result["users"]:
            return []
        return result["users"] 
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []

@query.field("user_by_username")
def resolve_name(user, info):
    return user.get("username")

@query.field("user_by_email")
def resolve_email(user, info):
    return user.get("email")

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