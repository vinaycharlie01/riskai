import os
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from logging_config import setup_logging

logger = setup_logging()

class MongoStore:
    """MongoDB-based job storage for distributed deployment"""
    
    def __init__(self):
        # Priority 1: Check for MONGO_URL (Railway or external MongoDB)
        mongo_url = os.getenv("MONGO_URL") or os.getenv("MONGO_PUBLIC_URL")
        
        if mongo_url:
            # Use the provided MongoDB URL (Railway, Atlas, etc.)
            self.mongo_uri = mongo_url
            # Always use the database name from env var or default
            # Don't extract from URL - create a new database if needed
            self.mongo_db = os.getenv("MONGO_DB", "risklens_ai")
            logger.info(f"🔗 Using MONGO_URL for connection")
            logger.info(f"📂 Will use/create database: {self.mongo_db}")
        else:
            # Priority 2: Build connection string from individual env vars (Kubernetes)
            mongo_host = os.getenv("MONGO_HOST") or os.getenv("MONGOHOST", "mongodb")
            mongo_port = int(os.getenv("MONGO_PORT") or os.getenv("MONGOPORT", "27017"))
            mongo_db = os.getenv("MONGO_DB", "risklens_ai")
            mongo_user = os.getenv("MONGO_USER") or os.getenv("MONGOUSER") or os.getenv("MONGO_INITDB_ROOT_USERNAME", "")
            mongo_password = os.getenv("MONGO_PASSWORD") or os.getenv("MONGOPASSWORD") or os.getenv("MONGO_INITDB_ROOT_PASSWORD", "")
            
            # Build connection string
            if mongo_user and mongo_password:
                self.mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
                logger.info(f"🔗 Using MongoDB with authentication: {mongo_host}:{mongo_port}")
            else:
                self.mongo_uri = f"mongodb://{mongo_host}:{mongo_port}"
                logger.info(f"🔗 Using MongoDB without authentication: {mongo_host}:{mongo_port}")
            
            self.mongo_db = mongo_db
        
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.jobs_collection = None
        
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(
                self.mongo_uri,
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            await self.client.admin.command('ping')
            
            self.db = self.client[self.mongo_db]
            self.jobs_collection = self.db.jobs
            
            # Create indexes for better performance using IndexModel
            from pymongo import IndexModel, ASCENDING
            
            indexes = [
                IndexModel([("job_id", ASCENDING)], unique=True, name="job_id_unique"),
                IndexModel([("status", ASCENDING)], name="status_index"),
                IndexModel([("blockchain_identifier", ASCENDING)], name="blockchain_id_index")
            ]
            
            # Create indexes asynchronously
            try:
                await self.jobs_collection.create_indexes(indexes)
                logger.info("✅ MongoDB indexes created successfully")
            except Exception as idx_error:
                # Indexes might already exist, which is fine
                logger.info(f"ℹ️  Index creation note: {str(idx_error)}")
            
            # Mask password in URI for logging
            safe_uri = self.mongo_uri
            if "@" in safe_uri and "://" in safe_uri:
                # mongodb://user:password@host:port -> mongodb://user:***@host:port
                parts = safe_uri.split("://")
                if "@" in parts[1]:
                    auth_and_host = parts[1].split("@")
                    if ":" in auth_and_host[0]:
                        user = auth_and_host[0].split(":")[0]
                        safe_uri = f"{parts[0]}://{user}:***@{auth_and_host[1]}"
            
            logger.info(f"✅ Connected to MongoDB successfully")
            logger.info(f"📂 Database: {self.mongo_db}")
            logger.info(f"🔗 Connection: {safe_uri}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def ping(self):
        """Ping MongoDB to check connection health"""
        if self.client:
            await self.client.admin.command('ping')
        else:
            raise Exception("MongoDB client not connected")
    
    async def set_job(self, job_id: str, job_data: Dict[str, Any]):
        """Store job data in MongoDB"""
        try:
            job_doc = {
                "job_id": job_id,
                **job_data
            }
            await self.jobs_collection.insert_one(job_doc)
            logger.info(f"Stored job {job_id} in MongoDB")
        except Exception as e:
            logger.error(f"Failed to store job {job_id}: {str(e)}")
            raise
    
    async def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve job data from MongoDB"""
        try:
            job_doc = await self.jobs_collection.find_one({"job_id": job_id})
            if job_doc:
                # Remove MongoDB's _id field
                job_doc.pop('_id', None)
                job_doc.pop('job_id', None)  # Remove duplicate job_id
                return job_doc
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve job {job_id}: {str(e)}")
            return None
    
    async def update_job(self, job_id: str, updates: Dict[str, Any]):
        """Update specific fields in job data"""
        try:
            result = await self.jobs_collection.update_one(
                {"job_id": job_id},
                {"$set": updates}
            )
            if result.modified_count > 0:
                logger.info(f"Updated job {job_id} in MongoDB")
            else:
                logger.warning(f"Job {job_id} not found for update")
        except Exception as e:
            logger.error(f"Failed to update job {job_id}: {str(e)}")
            raise
    
    async def delete_job(self, job_id: str):
        """Delete job data from MongoDB"""
        try:
            await self.jobs_collection.delete_one({"job_id": job_id})
            logger.info(f"Deleted job {job_id} from MongoDB")
        except Exception as e:
            logger.error(f"Failed to delete job {job_id}: {str(e)}")
    
    async def get_all_jobs(self, status: Optional[str] = None) -> list:
        """Get all jobs, optionally filtered by status"""
        try:
            query = {"status": status} if status else {}
            cursor = self.jobs_collection.find(query)
            jobs = await cursor.to_list(length=100)
            # Remove MongoDB _id field
            for job in jobs:
                job.pop('_id', None)
            return jobs
        except Exception as e:
            logger.error(f"Failed to retrieve jobs: {str(e)}")
            return []

# Global MongoDB store instance
mongo_store = MongoStore()

# Made with Bob
