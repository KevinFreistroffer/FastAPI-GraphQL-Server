from ariadne import ObjectType, gql, make_executable_schema, load_schema_from_path
# from .types.user_types import type_defs
# from .resolvers.user import query as user_query

# type_defs = gql(
#     """
#     type User {
#         _id: ID!
#         name: String!
#         username: String!
#         email: String!
#         fullname: String
#         createdAt: String!
#         isVerified: Boolean!
        
#     type Query {
#         users: [User]!
#         user(_id: ID!): User
#         userByUsername(username: String!): User
#         userByEmail(email: String!): User
#     }

#     type Mutation {
#         createUser(name: String!, username: String!, email: String!, password: String!): User
#         updateUser(_id: ID!, name: String, password: String): User
#         deleteUser(_id: ID!): Boolean!
#     }
# #     """
# )

# query = ObjectType("Query")

# @user_type.field("name")
# def resolve_name(user, info):
#     return user.get("name")

# @user_type.field("email")
# def resolve_email(user, info):
#     return user.get("email")

query = ObjectType("Query")
mutation = ObjectType("Mutation")
user = ObjectType("User")

@query.field("users")
def resolve_users(*_):
    try:
        users = get_all_users()
        if not users:
            return []
        return users 
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []


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
        
    type Query {
        users: [User]!
        user(_id: ID!): User
        userByUsername(username: String!): User
        userByEmail(email: String!): User
    }

    type Mutation {
        createUser(name: String!, username: String!, email: String!, password: String!): User
        updateUser(_id: ID!, name: String, password: String): User
        deleteUser(_id: ID!): Boolean!
    }
    """
)

schema = make_executable_schema(type_defs, query)