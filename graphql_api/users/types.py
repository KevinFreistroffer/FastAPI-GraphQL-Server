from ariadne import ObjectType, gql, make_executable_schema

type_defs = gql(
    """
    type User {
        _id: ID!
        name: String!
        username: String!
        email: String!
        fullname: String
        createdAt: String!
        isVerified: Boolean!
    }
    """
)
# user_type_defs = gql(
#     """
#     type User {
#         _id: ID!
#         name: String!
#         username: String!
#         email: String!
#         fullname: String
#         createdAt: String!
#         isVerified: Boolean!
#     }

#     type Query {
#         users: [User]!
#         user(_id: ID!): User
#         userByUsername(username: String!): User
#         userByEmail(email: String!): User
#     }
#     """
# )


# query = ObjectType("Query")

# @query.field("users")
# def resolve_users(*_):
#     try:
#         result = get_all_users()
#         if not result["users"]:
#             return []
#         return result["users"] 
#     except Exception as e:
#         print(f"Error fetching users: {e}")
#         return []

# @query.field("userByUsername")
# def resolve_name(user, info):
#     return user.get("username")

# @query.field("email")
# def resolve_email(user, info):
#     return user.get("email")