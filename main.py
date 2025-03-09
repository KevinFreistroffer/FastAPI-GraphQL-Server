from typing import Union
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import JSONResponse
from schemas.User import UserCreate, UserUpdate
from operations.user_operations import create_user, get_all_users, get_user_by_id, get_user_by_name, update_user
from pymongo.errors import PyMongoError
from defs.status_codes import StatusCode, create_error_response
from graphql_api.schema import schema
from ariadne import load_schema_from_path
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
import logging
import os
import pymongo
from bson.json_util import dumps
import asyncio
import json
from utils.watch_mongodb import watch_mongodb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start watcher in background task
    logger.info("Starting lifespan")
    watcher_task = asyncio.create_task(watch_mongodb())
    logger.info("Watcher task created")
    
    yield
    
    # Cleanup
    logger.info("Shutting down watcher")
    watcher_task.cancel()
    try:
        await watcher_task
    except asyncio.CancelledError:
        logger.info("Watcher stopped")

app = FastAPI(lifespan=lifespan)
app.mount("/api/graphql", GraphQL(schema, debug=True))

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application starting up")

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