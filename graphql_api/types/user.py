from ariadne import ObjectType, gql, make_executable_schema

user = gql("""
    type Query {
        users: UsersResult
        user_by_id(_id: ID!): UserResult
        user_by_username(username: String!): UserResult
        user_by_email(email: String!): UserResult
        login(username: String, email: String, password: String!): LoginResult
    }

    type Mutation {
        create_user(name: String!, username: String!, email: String!, password: String!): UserResult
        update_user(_id: ID!, name: String, password: String): UserResult
        delete_user(_id: ID!): Boolean!
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

    type UserResult {
        user: User
        error: String
    }

    type UsersResult {
        users: [User]!
        error: String
    }

    type LoginResult {
        success: Boolean!,
        error: String
    }
""")

