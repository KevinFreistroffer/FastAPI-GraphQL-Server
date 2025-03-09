import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from functools import lru_cache
from bson import ObjectId
import json
from json import JSONEncoder
from bson import ObjectId

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')

exclude_fields = { "password": 0 }

@lru_cache()
def get_database():
    """
    Get MongoDB database connection.
    Uses lru_cache to maintain a single connection instance.
    """
    try:
        # Create a new client and connect to the server
        client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        # Test connection
        client.admin.command('ping')
        print("Connected to MongoDB!")
        # Return database
        return client.get_database('journal')  # Replace 'journal' with your database name
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

# Helper functions for common operations
def get_collection(collection_name: str):
    """Get a MongoDB collection by name."""
    db = get_database()
    return db[collection_name]

# Add this helper function to convert MongoDB documents to JSON-serializable format
def serialize_document(doc):
    """Convert MongoDB document to JSON-serializable format."""
    if isinstance(doc, ObjectId):
        return str(doc)
    if isinstance(doc, dict):
        return {k: serialize_document(v) for k, v in doc.items()}
    if isinstance(doc, list):
        return [serialize_document(item) for item in doc]
    return doc

# Example usage functions
def insert_one(collection_name: str, document: dict):
    """Insert a single document into a collection."""
    collection = get_collection(collection_name)
    result = collection.insert_one(document)
    return result
    return {"_id": str(result.inserted_id)}  # Convert ObjectId to string

def find_one(collection_name: str, query: dict):
    print("find_one", query)
    """Find a single document in a collection."""

    if '_id' in query and isinstance(query['_id'], str):
        query['_id'] = ObjectId(query['_id'])
    collection = get_collection(collection_name)
    result = collection.find_one(query, exclude_fields)
    return serialize_document(result) if result else None

def find_many(collection_name: str, query: dict = None):
    """Find multiple documents in a collection."""
    collection = get_collection(collection_name)
    results = list(collection.find(query or {}, exclude_fields))
    return serialize_document(results)

def update_one(collection_name: str, query: dict, update: dict):
    """Update a single document in a collection."""
    print("update_one", query, update)
    collection = get_collection(collection_name)
    return collection.update_one(query, {"$set": update}) 