# from graphql_api.users.types import type_defs as user_type_defs
# from graphql_api.users.resolvers import user as user_resolvers, query as user_query_resolvers
from graphql_api.types import types
from graphql_api.resolvers import resolvers
from ariadne.asgi import GraphQL
from ariadne import ObjectType, gql, make_executable_schema, load_schema_from_path

mutation = ObjectType("Mutation")

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
        
    type Mutation {
        createUser(name: String!, username: String!, email: String!, password: String!): User
        updateUser(_id: ID!, name: String, password: String): User
        deleteUser(_id: ID!): Boolean!
    }

    type Query {
        users: [User]!
        user(_id: ID!): User
        userByUsername(username: String!): User
        userByEmail(email: String!): User
    }
    """
)

schema = make_executable_schema(types, resolvers)