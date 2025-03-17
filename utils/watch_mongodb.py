from motor.motor_asyncio import AsyncIOMotorClient
import logging
import os
import asyncio
import json
import boto3
from utils.database import serialize_document
from bson import json_util  # For MongoDB serialization

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def watch_mongodb():
    logger.info("Starting MongoDB watch")
    client = AsyncIOMotorClient(os.getenv('MONGODB_URI'))
    
    try:
        # Watch for both inserts and updates
        pipeline = [{
            '$match': {
                '$or': [
                    {'operationType': 'insert'},
                    {'operationType': 'update'}
                ]
            }
        }]
        
        while True:
            try:
                collection = client.journal.users
                logger.info(f"Watching collection: {collection.name}")
                
                change_stream = collection.watch(
                    pipeline,
                    full_document='updateLookup'
                )
                
                # logger.info("Change stream created, waiting for changes...")
                
                async for change in change_stream:
                    # logger.info(f"Change detected: {json.dumps(change, default=str)}")
                    
                    if change['operationType'] == 'insert':
                        user = change['fullDocument']
                        logger.info(f"New user created: {user.get('email')}")
                        
                        # Clean and serialize the user document
                        user_dict = json.loads(json_util.dumps(user))  # Convert MongoDB doc to dict
                        
                        # Remove sensitive data
                        if 'password' in user_dict:
                            del user_dict['password']
                        
                        payload = {
                            "body": {
                                "user": user_dict,
                                "email": "kevin.freistroffer@gmail.com"
                            }
                        }
                        
                        # Convert to JSON string and then to bytes for Lambda
                        lambda_payload = json.dumps(payload).encode('utf-8')
                        
                        session = boto3.Session(profile_name="AdministratorAccess-211125458425")
                        lambda_client = session.client('lambda')
                        lambda_client.invoke(
                            FunctionName="NewAccount-dev-send_email",
                            InvocationType='Event',
                            Payload=lambda_payload
                        )
                        
                    elif change['operationType'] == 'update':
                        # Handle user update
                        user = change['fullDocument']
                        updated_fields = []
                        
                        # Check which fields were updated
                        if 'updateDescription' in change:
                            updated_fields = list(change['updateDescription']['updatedFields'].keys())
                            
                        # Only send email if name or password was updated
                        if any(field in ['name', 'password'] for field in updated_fields):
                            logger.info(f"User updated: {user.get('email')}, Fields: {updated_fields}")
                            
                            # Clean and serialize the user document
                            user_dict = json.loads(json_util.dumps(user))  # Convert MongoDB doc to dict
                            
                            # Remove sensitive data
                            if 'password' in user_dict:
                                del user_dict['password']

                            payload = {
                                "body": {
                                    "user": user_dict,
                                    # "email": user['email'],
                                    "email": "kevin.freistroffer@gmail.com",
                                    "updated_fields": updated_fields
                                }
                            }
                            
                            # Send update notification email
                            session = boto3.Session(profile_name="AdministratorAccess-211125458425")
                            lambda_client = session.client('lambda')
                            lambda_client.invoke(
                                FunctionName="AccountUpdated-dev-send_email",
                                InvocationType='Event',
                                Payload=json.dumps(payload).encode('utf-8')
                            )
                    
            except Exception as e:
                logger.error(f"Stream error: {e}")
                await asyncio.sleep(1)
                
    except Exception as e:
        logger.error(f"Watch error: {e}")
        raise
