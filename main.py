from typing import Union
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from schemas.Simple import UserCreate, UserUpdate
from operations.user_operations import create_user, get_all_users, get_user_by_id, get_user_by_name, update_user
from pymongo.errors import PyMongoError
from defs.status_codes import StatusCode, create_error_response
from graphql_api.schema import schema
from graphql_api.types.user_types import user_type_defs
from ariadne.asgi import GraphQL
from ariadne import ObjectType, gql, make_executable_schema, load_schema_from_path
print(user_type_defs)
query = ObjectType("Query")
mutation = ObjectType("Mutation")
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

schema = make_executable_schema(type_defs, query)


# type_defs = [
#     base_defs,
#     user_type_defs,
#     user_query_defs
# ]

app = FastAPI()
app.mount("/api/graphql", GraphQL(schema, debug=True))

@app.post("/api/user/create")
def create_user_handler(user: UserCreate, response: Response):
    try:
        result = create_user(user)
        if "error" in result:
            return JSONResponse(
                status_code=result["status_code"],
                content={"error": "Could not create the user"}
            )
        return result
    except PyMongoError as e:
        print("e",)
        raise HTTPException(
            status_code=StatusCode.CAUGHT_ERROR.value,
            detail=f"An error occurred. Try again later."
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=StatusCode.CAUGHT_ERROR.value,
            detail=f"Unexpected error:. Try again, or contact support."
        )

@app.get("/api/users")
def get_users_handler():
    try:
        result = get_all_users()
        if "error" in result:
            raise HTTPException(
                status_code=result["status_code"],
                detail=result["error"]
            )
        return result
    except PyMongoError as e:
        raise HTTPException(
            status_code=StatusCode.CAUGHT_ERROR.value,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=StatusCode.CAUGHT_ERROR.value,
            detail=f"Unexpected error: {str(e)}"
        )

@app.get("/api/user/id/{id}")
def get_user_by_id_handler(id: str):
    try:
        result = get_user_by_id(id)
        if "error" in result:
            raise HTTPException(
                status_code=result["status_code"],
                detail=result["error"]
            )
        return result
    except PyMongoError as e:
        raise HTTPException(
            status_code=StatusCode.CAUGHT_ERROR.value,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=StatusCode.CAUGHT_ERROR.value,
            detail=f"Unexpected error: {str(e)}"
        )

@app.get("/api/user/name/{name}")
def get_user_by_name_handler(name: str):
    try:
        result = get_user_by_name(name)
        if "error" in result:
            raise HTTPException(
                status_code=result["status_code"],
                detail=result["error"]
            )
        return result
    except PyMongoError as e:
        raise HTTPException(
            status_code=StatusCode.CAUGHT_ERROR.value,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=StatusCode.CAUGHT_ERROR.value,
            detail=f"Unexpected error: {str(e)}"
        )

@app.put("/api/user")
def update_user_handler(user: UserUpdate):
    try:
        result = update_user(user)
        if "error" in result:
            raise HTTPException(
                status_code=result["status_code"],
                detail=result["error"]
            )
        return result
    except PyMongoError as e:
        raise HTTPException(
            status_code=StatusCode.CAUGHT_ERROR.value,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=StatusCode.CAUGHT_ERROR.value,
            detail=f"Unexpected error: {str(e)}"
        )