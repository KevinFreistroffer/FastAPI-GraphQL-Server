from ariadne import ObjectType, gql, make_executable_schema

query = ObjectType("Query")
user = ObjectType("User")

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

@query.field("userByUsername")
def resolve_name(user, info):
    return user.get("username")

@query.field("email")
def resolve_email(user, info):
    return user.get("email")