from typing import Union
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from schemas.Simple import UserCreate, UserUpdate
from operations.user_operations import create_user, get_all_users, get_user_by_id, get_user_by_name, update_user
from pymongo.errors import PyMongoError
from defs.status_codes import StatusCode, create_error_response


app = FastAPI(prefix="/api")

@app.post("/user/create")
def create_user_handler(user: UserCreate, response: Response):
    try:
        result = create_user(user)
        print("result", result)
        if "error" in result:
            return JSONResponse(
                status_code=result["status_code"],
                content={"error": "Could not created the user"}
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

@app.get("/users")
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

@app.get("/user/id/{id}")
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

@app.get("/user/name/{name}")
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

@app.put("/user")
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