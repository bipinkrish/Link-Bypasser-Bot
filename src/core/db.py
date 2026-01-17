try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, DuplicateKeyError
    MONGODB_AVAILABLE = True
except ImportError:
    MongoClient = None
    ConnectionFailure = None
    DuplicateKeyError = None
    MONGODB_AVAILABLE = False

from datetime import datetime
import os
import hashlib

class DB:
    def __init__(self, connection_string=None, db_name="linkbypasser", collection_name="results") -> None:
        """
        Initialize MongoDB connection for Link Bypasser Bot
        
        Args:
            connection_string: MongoDB connection string (default: from env MONGODB_URI)
            db_name: Database name (default: "linkbypasser")  
            collection_name: Collection name (default: "results")
        """
        if not MONGODB_AVAILABLE:
            raise Exception("PyMongo not available. Install with: pip install pymongo")
            
        # Get connection string from environment or parameter
        self.connection_string = connection_string or os.getenv('MONGODB_URI')
        if not self.connection_string:
            # Default to local MongoDB if no connection string provided
            self.connection_string = "mongodb://localhost:27017/"
            
        self.db_name = db_name
        self.collection_name = collection_name
        
        try:
            # Initialize MongoDB client
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database and collection
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            
            # Create indexes for better performance
            self.collection.create_index("link", unique=True)
            self.collection.create_index("created_at")
            self.collection.create_index("link_hash")
            
            print(f"✅ Connected to MongoDB: {self.db_name}.{self.collection_name}")
            
        except ConnectionFailure as e:
            raise Exception(f"Failed to connect to MongoDB: {e}")
        except Exception as e:
            raise Exception(f"MongoDB initialization error: {e}")

    def _hash_link(self, link: str) -> str:
        """Create a hash of the link for faster lookups"""
        return hashlib.md5(link.encode()).hexdigest()

    def insert(self, link: str, result: str) -> bool:
        """
        Insert a link and its bypass result into the database
        
        Args:
            link: Original shortened/protected link
            result: Bypassed/direct link result
            
        Returns:
            bool: True if inserted successfully, False otherwise
        """
        try:
            document = {
                "link": link,
                "link_hash": self._hash_link(link),
                "result": result,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Use upsert to update if exists, insert if new
            filter_query = {"link": link}
            update_query = {
                "$set": document,
                "$setOnInsert": {"created_at": datetime.utcnow()}
            }
            
            result = self.collection.update_one(
                filter_query, 
                update_query, 
                upsert=True
            )
            
            return True
            
        except Exception as e:
            print(f"Error inserting to MongoDB: {e}")
            return False

    def find(self, link: str) -> str:
        """
        Find the bypass result for a given link
        
        Args:
            link: Original shortened/protected link to search for
            
        Returns:
            str: Bypassed result if found, None otherwise
        """
        try:
            # First try exact link match
            document = self.collection.find_one({"link": link})
            
            if document:
                # Update access time for cache management
                self.collection.update_one(
                    {"_id": document["_id"]},
                    {"$set": {"last_accessed": datetime.utcnow()}}
                )
                return document.get("result")
                
            # Fallback: try hash-based lookup for performance
            link_hash = self._hash_link(link)
            document = self.collection.find_one({"link_hash": link_hash})
            
            if document:
                self.collection.update_one(
                    {"_id": document["_id"]},
                    {"$set": {"last_accessed": datetime.utcnow()}}
                )
                return document.get("result")
                
            return None
            
        except Exception as e:
            print(f"Error finding in MongoDB: {e}")
            return None
            
    def get_stats(self) -> dict:
        """Get database statistics"""
        try:
            total_links = self.collection.count_documents({})
            
            # Get recent activity (last 24 hours)
            from datetime import timedelta
            yesterday = datetime.utcnow() - timedelta(days=1)
            recent_count = self.collection.count_documents({
                "created_at": {"$gte": yesterday}
            })
            
            return {
                "total_links": total_links,
                "recent_links_24h": recent_count,
                "database": self.db_name,
                "collection": self.collection_name
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}
            
    def cleanup_old_entries(self, days_old: int = 30) -> int:
        """Remove entries older than specified days"""
        try:
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            result = self.collection.delete_many({
                "created_at": {"$lt": cutoff_date}
            })
            
            print(f"🧹 Cleaned up {result.deleted_count} old entries")
            return result.deleted_count
            
        except Exception as e:
            print(f"Error cleaning up: {e}")
            return 0
            
    def close(self):
        """Close the MongoDB connection"""
        if hasattr(self, 'client'):
            self.client.close()
            print("📴 MongoDB connection closed")
