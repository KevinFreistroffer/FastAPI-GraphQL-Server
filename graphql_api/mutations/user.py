from ariadne import ObjectType, gql, make_executable_schema

# query = ObjectType("Query")
mutation = ObjectType("Mutation")
# user = ObjectType("User")

# @query.field("users")
# def resolve_users(*_):
#     try:
#         users = get_all_users()
#         if not users:
#             return []
#         return users 
#     except Exception as e:
#         print(f"Error fetching users: {e}")
#         return []

# @query.field("userByUsername")
# def resolve_name(user, info):
#     return user.get("username")

# @query.field("email")
# def resolve_email(user, info):
#     return user.get("email")