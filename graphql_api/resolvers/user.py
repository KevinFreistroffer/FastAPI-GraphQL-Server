from ariadne import ObjectType, gql, make_executable_schema
from operations.user_operations import get_all_users
from operations.user_operations import create_user
from schemas.User import UserCreate
from graphql import GraphQLError


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

"""
        createUser(name: String!, username: String!, email: String!, password: String!): User
        updateUser(_id: ID!, name: String, password: String): User
        deleteUser(_id: ID!): Boolean!
"""
@mutation.field("create_user")
def resolve_create_user(_, info, **user_info):
    print("user_info", user_info)
    try:
        user = UserCreate(**user_info)
        print("user", user)
        result = create_user(user)
        print("result", result)

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

    except ValueError as e:
        print("ValueError e", e)
        return {
            "user": None,
            "error": str(e)
        }
    except Exception as e:
        print("Exception e", e)
        return {
            "user": None,
            "error": str(e)
        }