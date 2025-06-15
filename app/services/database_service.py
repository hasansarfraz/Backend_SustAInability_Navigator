# app/services/database_service.py - Database service stub

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import logging
# from motor.motor_asyncio import AsyncIOMotorClient  # For MongoDB
# Or use: from sqlalchemy.ext.asyncio import AsyncSession  # For SQL databases

logger = logging.getLogger(__name__)

class DatabaseService:
    """
    Database service for managing users, chats, and messages.
    
    This is a stub implementation. You'll need to:
    1. Choose your database (MongoDB, PostgreSQL, etc.)
    2. Set up the connection
    3. Implement the actual database operations
    """
    
    def __init__(self):
        # Initialize your database connection here
        # Example for MongoDB:
        # self.client = AsyncIOMotorClient("mongodb://localhost:27017")
        # self.db = self.client.sustainability_navigator
        
        # For now, using in-memory storage for testing
        self.users = {}
        self.chats = {}
        self.messages = {}
    
    async def get_user_id_from_chat(self, chat_id: str) -> str:
        """
        Get user ID associated with a chat session.
        
        In production, this would query your database.
        """
        # Stub implementation
        # In reality, you'd query: SELECT user_id FROM chats WHERE chat_id = ?
        
        # For testing, extract user_id from chat_id pattern
        # Assuming chat_id format: "user123_chat456"
        if "_" in chat_id:
            return chat_id.split("_")[0]
        
        # Or implement your own logic
        return "default_user"
    
    async def get_user_params(self, user_id: str) -> Dict:
        """
        Retrieve user parameters from database.
        
        Path: /users/[uid]/params
        """
        # Stub implementation
        # In reality: SELECT params FROM users WHERE user_id = ?
        
        # Default params for testing
        default_params = {
            "persona": "general",
            "sustainability_proficiency": "intermediate",
            "technological_proficiency": "intermediate",
            "company_size": "Medium (100-500 employees)",
            "industry": "Manufacturing",
            "communication_style": "professional",
            "regulatory_importance": "high",
            "budget_priority": "medium",
            "preferred_language": "en"
        }
        
        return self.users.get(user_id, {}).get("params", default_params)
    
    async def save_user_params(self, user_id: str, params: Dict) -> None:
        """
        Save user parameters to database.
        
        Path: /users/[uid]/params
        """
        # Stub implementation
        # In reality: UPDATE users SET params = ? WHERE user_id = ?
        
        if user_id not in self.users:
            self.users[user_id] = {}
        
        self.users[user_id]["params"] = params
        logger.info(f"Saved params for user {user_id}")
    
    async def save_chat_message(
        self, 
        chat_id: str, 
        user_id: str, 
        message: str, 
        response: Dict
    ) -> None:
        """
        Save chat message and response to database.
        """
        # Stub implementation
        # In reality: INSERT INTO messages (chat_id, user_id, message, response, timestamp)
        
        timestamp = datetime.now()
        
        # Save to chats collection
        if chat_id not in self.chats:
            self.chats[chat_id] = {
                "chat_id": chat_id,
                "user_id": user_id,
                "created_at": timestamp,
                "updated_at": timestamp,
                "first_message": message,
                "title": self._generate_chat_title(message),
                "message_count": 0
            }
        
        # Update chat metadata
        self.chats[chat_id]["updated_at"] = timestamp
        self.chats[chat_id]["message_count"] += 1
        
        # Save message
        message_id = f"{chat_id}_{timestamp.timestamp()}"
        self.messages[message_id] = {
            "message_id": message_id,
            "chat_id": chat_id,
            "user_id": user_id,
            "user_message": message,
            "ai_response": response,
            "timestamp": timestamp
        }
    
    async def get_user_chats(self, user_id: str, start_date: str) -> List[Dict]:
        """
        Retrieve user's chat history from a specific date.
        
        Args:
            user_id: User ID
            start_date: Start date in YYYY-MM-DD format
        
        Returns:
            List of chat summaries
        """
        # Parse start date
        try:
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            start_datetime = datetime.now() - timedelta(days=30)
        
        # Stub implementation
        # In reality: SELECT * FROM chats WHERE user_id = ? AND created_at >= ?
        
        user_chats = []
        for chat_id, chat_data in self.chats.items():
            if (chat_data.get("user_id") == user_id and 
                chat_data.get("created_at", datetime.now()) >= start_datetime):
                user_chats.append(chat_data)
        
        # Sort by date descending
        user_chats.sort(key=lambda x: x.get("created_at", datetime.now()), reverse=True)
        
        return user_chats
    
    def _generate_chat_title(self, first_message: str) -> str:
        """
        Generate a chat title from the first message.
        """
        # Simple title generation
        if len(first_message) <= 50:
            return first_message
        
        # Find a good break point
        title = first_message[:50]
        last_space = title.rfind(" ")
        if last_space > 30:
            title = title[:last_space]
        
        return title + "..."

# Create global instance
db_service = DatabaseService()


# Example MongoDB implementation (commented out):
"""
class MongoDBService(DatabaseService):
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.sustainability_navigator
        self.users_collection = self.db.users
        self.chats_collection = self.db.chats
        self.messages_collection = self.db.messages
    
    async def get_user_params(self, user_id: str) -> Dict:
        user = await self.users_collection.find_one({"_id": user_id})
        if user and "params" in user:
            return user["params"]
        return {}
    
    async def save_user_params(self, user_id: str, params: Dict) -> None:
        await self.users_collection.update_one(
            {"_id": user_id},
            {"$set": {"params": params, "updated_at": datetime.now()}},
            upsert=True
        )
    
    async def get_user_id_from_chat(self, chat_id: str) -> str:
        chat = await self.chats_collection.find_one({"_id": chat_id})
        if chat:
            return chat.get("user_id", "unknown")
        raise ValueError(f"Chat {chat_id} not found")
    
    async def save_chat_message(self, chat_id: str, user_id: str, message: str, response: Dict) -> None:
        # Update or create chat
        await self.chats_collection.update_one(
            {"_id": chat_id},
            {
                "$set": {
                    "user_id": user_id,
                    "updated_at": datetime.now()
                },
                "$setOnInsert": {
                    "created_at": datetime.now(),
                    "first_message": message,
                    "title": self._generate_chat_title(message)
                },
                "$inc": {"message_count": 1}
            },
            upsert=True
        )
        
        # Save message
        await self.messages_collection.insert_one({
            "chat_id": chat_id,
            "user_id": user_id,
            "user_message": message,
            "ai_response": response,
            "timestamp": datetime.now()
        })
    
    async def get_user_chats(self, user_id: str, start_date: str) -> List[Dict]:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        
        cursor = self.chats_collection.find({
            "user_id": user_id,
            "created_at": {"$gte": start_datetime}
        }).sort("created_at", -1)
        
        chats = []
        async for chat in cursor:
            chats.append({
                "chat_id": str(chat["_id"]),
                "title": chat.get("title", "Untitled"),
                "created_at": chat["created_at"],
                "message_count": chat.get("message_count", 0)
            })
        
        return chats
"""