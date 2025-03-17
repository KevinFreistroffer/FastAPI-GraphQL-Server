from typing import Union, List, Dict, Any, Optional
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
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection string
MONGODB_URI = "mongodb+srv://admin:y1Xa7bylHknE2sWs@cluster0.wbjpx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "matrix-datasets"
COLLECTION_NAME = "matrix-datasets"

# Pydantic models
class DatasetBase(BaseModel):
    name: str
    description: str = None
    data: Dict[str, Any] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DatasetCreate(BaseModel):
    name: str
    description: Optional[str] = None
    
    # Allow any additional fields
    class Config:
        extra = "allow"

class DatasetUpdate(BaseModel):
    id: str
    name: str = None
    description: str = None
    data: Dict[str, Any] = None
    metadata: Dict[str, Any] = None

# Database client
client = None
db = None
collection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup: connect to MongoDB
    global client, db, collection
    logger.info("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    logger.info(f"Connected to MongoDB database: {DB_NAME}, collection: {COLLECTION_NAME}")
    
    # Start watcher in background task
    logger.info("Starting lifespan")
    watcher_task = asyncio.create_task(watch_mongodb())
    logger.info("Watcher task created")
    
    yield
    
    # Cleanup: close MongoDB connection
    logger.info("Closing MongoDB connection...")
    client.close()
    logger.info("MongoDB connection closed")
    
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
def get_users():
    try:
        with Session(engine) as session:
            stmt = select(User)
            result = session.execute(stmt)
            users = [row[0].to_dict() for row in result]
            return {"users": users}
    except Exception as e:
        print(e)
        return {"users": []}

@app.get("/api/user/id/{id}")
def get_user_by_id(id: int):
    try:
        with Session(engine) as session:
            stmt = select(User).where(User.id == id)
            result = session.execute(stmt).first()
            if result:
                user = result[0]
                return {
                    "id": user.id,
                    "name": user.name,
                    "fullname": user.fullname
                }
            return {"error": "User not found"}
    except Exception as e:
        print(e)
        return {"error": str(e)}

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

@app.get("/")
async def root():
    return {"message": "Welcome to Matrix Datasets API"}

@app.post("/api/datasets", response_model=Dict[str, Any])
async def create_dataset(dataset: Dict[str, Any]):
    """
    Create a new dataset with completely dynamic fields.
    MongoDB will store whatever is in the dataset dict.
    """

    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    print("dataset", dataset)
    try:
        # Add metadata
        dataset["created_at"] = datetime.utcnow()
        dataset["_id"] = str(uuid.uuid4())
        
        # Insert into MongoDB
        result = await db.datasets.insert_one(dataset)

        print("result", result)
        
        return {
            "status": "success",
            "message": "Dataset created successfully",
            "dataset_id": dataset["_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create dataset: {str(e)}")

@app.get("/api/datasets", response_model=List[Dict[str, Any]])
async def get_all_datasets():
    try:
        datasets = []
        cursor = collection.find({})
        async for document in cursor:
            document["id"] = str(document.pop("_id"))
            datasets.append(document)
        return datasets
    except PyMongoError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@app.get("/api/datasets/{dataset_id}", response_model=Dict[str, Any])
async def get_dataset_by_id(dataset_id: str):
    try:
        from bson.objectid import ObjectId
        
        dataset = await collection.find_one({"_id": ObjectId(dataset_id)})
        if dataset:
            dataset["id"] = str(dataset.pop("_id"))
            return dataset
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Dataset with ID {dataset_id} not found"
            )
    except PyMongoError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@app.put("/api/datasets/{dataset_id}", response_model=Dict[str, Any])
async def update_dataset(dataset_id: str, dataset: DatasetUpdate):
    try:
        from bson.objectid import ObjectId
        
        update_data = {k: v for k, v in dataset.model_dump().items() 
                      if v is not None and k != "id"}
        
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No valid update data provided"
            )
        
        result = await collection.update_one(
            {"_id": ObjectId(dataset_id)},
            {"$set": update_data}
        )
        
        if result.matched_count:
            updated_dataset = await collection.find_one({"_id": ObjectId(dataset_id)})
            updated_dataset["id"] = str(updated_dataset.pop("_id"))
            return updated_dataset
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Dataset with ID {dataset_id} not found"
            )
    except PyMongoError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@app.delete("/api/datasets/{dataset_id}", response_model=Dict[str, str])
async def delete_dataset(dataset_id: str):
    try:
        from bson.objectid import ObjectId
        
        result = await collection.delete_one({"_id": ObjectId(dataset_id)})
        
        if result.deleted_count:
            return {"message": f"Dataset with ID {dataset_id} deleted successfully"}
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Dataset with ID {dataset_id} not found"
            )
    except PyMongoError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )