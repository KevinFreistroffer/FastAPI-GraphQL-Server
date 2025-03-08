from ariadne import ObjectType, gql, make_executable_schema

user = gql(
    """
    type Query {
        users: [User]!
        user(_id: ID!): User
        user_by_username(username: String!): User
        user_by_email(email: String!): User
    }

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
        create_user(name: String!, username: String!, email: String!, password: String!): CreateUserResult
        update_user(_id: ID!, name: String, password: String): User
        delete_user(_id: ID!): Boolean!
    }

    type CreateUserResult {
        user: User
        error: String
    }

    # extend type Mutation {
    #     createUser(
    #         name: String!,
    #         username: String!,
    #         email: String!,
    #         password: String!
    #     ): CreateUserResult
    # }

    """
)