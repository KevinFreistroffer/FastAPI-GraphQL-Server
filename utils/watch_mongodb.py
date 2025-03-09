from motor.motor_asyncio import AsyncIOMotorClient
import logging
import os
import asyncio
import json
import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def watch_mongodb():
    logger.info("Starting MongoDB watch")
    client = AsyncIOMotorClient(os.getenv('MONGODB_URI'))
    
    try:
        # Specify pipeline to watch for inserts
        pipeline = [{'$match': {'operationType': 'insert'}}]
        
        while True:
            try:
                # Get specific database and collection
                collection = client.journal.users  # Adjust to your db/collection names
                logger.info(f"Watching collection: {collection.name}")
                
                # Create change stream with full document
                change_stream = collection.watch(
                    pipeline,
                    full_document='updateLookup'
                )
                
                logger.info("Change stream created, waiting for changes...")
                
                async for change in change_stream:
                    logger.info(f"Change detected: {json.dumps(change, default=str)}")
                    
                    # Get the full document
                    if 'fullDocument' in change:
                        user = change['fullDocument']
                        logger.info(f"New user created: {user.get('email')}")
                        
                        # Here you can trigger your email Lambda
                        # ... email Lambda code ...
                        session = boto3.Session(profile_name="AdministratorAccess-211125458425")
                        client = session.client('lambda')
                        body = b'{"body": {"user": {"_id": "65f4c8a12345678901234567", "name": "John Doe", "username": "johndoe", "email": "john.doe@example.com", "createdAt": "2024-03-15T10:30:00Z", "isVerified": false}, "email": "kevin.freistroffer@gmail.com"}}'
                        client.invoke_async(
                            FunctionName="EmailService-dev-send_email",
                            InvokeArgs=body
                        )
                    
            except Exception as e:
                logger.error(f"Stream error: {e}")
                await asyncio.sleep(1)  # Wait before reconnecting
                
    except Exception as e:
        logger.error(f"Watch error: {e}")
        raise  # Re-raise to see the full error
