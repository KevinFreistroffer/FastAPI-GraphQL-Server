from ariadne import ObjectType, gql, make_executable_schema


user = gql("""
    type Query {
        users: UsersResult
        user(_id: ID!): UserResult
        user_by_username(username: String!): UserResult
        user_by_email(email: String!): UserResult
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
        create_user(name: String!, username: String!, email: String!, password: String!): UserResult
        update_user(_id: ID!, name: String, password: String): UserResult
        delete_user(_id: ID!): Boolean!
    }

    type UserResult {
        user: User
        error: String
    }

    type UsersResult {
        users: [User]!
        error: String
    }

    extend type Mutation {
        createUser(
            username: String!
            password: String!
            email: String!
            name: String
        ): User

        updateUser(
            _id: ID!
            password: String!
            name: String
        ): User
    }
""")

