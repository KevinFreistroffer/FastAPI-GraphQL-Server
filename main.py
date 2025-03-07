from typing import Union
from fastapi import FastAPI, HTTPException
from schemas.Simple import UserCreate, UserUpdate
from operations.user import create_new_user, get_all_users, get_user_by_id, get_user_by_name, update_user
from pymongo.errors import PyMongoError
from defs.status_codes import StatusCode, create_error_response


app = FastAPI(prefix="/api")

@app.post("/user/create")
def create_user(user: UserCreate):
    try:
        result = create_new_user(user)
        if "error" in result:
            raise HTTPException(
                status_code=StatusCode.ERROR_INSERTING_USER.value,
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

@app.get("/users")
def get_users():
    try:
        result = get_all_users()
        if not result["users"]:
            raise HTTPException(
                status_code=StatusCode.USERS_NOT_FOUND.value,
                detail="No users found"
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

@app.get("/user/id/{id}")
def get_user_by_id(id: str):
    try:
        result = get_user_by_id(id)
        if "error" in result:
            raise HTTPException(
                status_code=StatusCode.USER_NOT_FOUND.value,
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

@app.get("/user/name/{name}")
def get_user_by_name(name: str):
    try:
        result = get_user_by_name(name)
        if "error" in result:
            raise HTTPException(
                status_code=StatusCode.USER_NOT_FOUND.value,
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

@app.put("/user")
def update_user(user: UserUpdate):
    try:
        result = update_user(user)
        if "error" in result:
            raise HTTPException(
                status_code=StatusCode.COULD_NOT_UPDATE.value,
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