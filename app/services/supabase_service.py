# app/services/supabase_service.py - Supabase implementation

import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class SupabaseService:
    """
    Supabase implementation for SustAInability Navigator.
    
    Supabase provides:
    - PostgreSQL database
    - Realtime subscriptions
    - Built-in authentication
    - Row Level Security (RLS)
    - Auto-generated APIs
    """
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Supabase URL and key must be set in environment variables")
        
        self.client: Client = create_client(self.url, self.key)
        logger.info("Supabase client initialized")
    
    async def setup_tables(self):
        """
        Create tables if they don't exist.
        Run this once or use Supabase dashboard to create tables.
        """
        # Note: Usually you'd create tables via Supabase dashboard or migrations
        # This is just for reference
        
        sql_commands = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                email TEXT UNIQUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                params JSONB DEFAULT '{}'::jsonb
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS chats (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                chat_id TEXT UNIQUE NOT NULL,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                title TEXT,
                first_message TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                message_count INTEGER DEFAULT 0
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS messages (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                chat_id TEXT REFERENCES chats(chat_id) ON DELETE CASCADE,
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                user_message TEXT NOT NULL,
                ai_response JSONB NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_chats_user_id ON chats(user_id);
            CREATE INDEX IF NOT EXISTS idx_messages_chat_id ON messages(chat_id);
            CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
            """
        ]
        
        # Execute via Supabase SQL editor or migrations
        logger.info("Tables should be created via Supabase dashboard")
    
    async def get_user_id_from_chat(self, chat_id: str) -> str:
        """Get user ID associated with a chat session."""
        try:
            response = self.client.table('chats').select('user_id').eq('chat_id', chat_id).single().execute()
            
            if response.data:
                return response.data['user_id']
            else:
                # For new chats, you might want to create a new user or use session
                logger.warning(f"No user found for chat {chat_id}")
                return await self._create_anonymous_user()
                
        except Exception as e:
            logger.error(f"Error getting user from chat: {e}")
            raise
    
    async def get_user_params(self, user_id: str) -> Dict:
        """Retrieve user parameters from database."""
        try:
            response = self.client.table('users').select('params').eq('id', user_id).single().execute()
            
            if response.data and response.data.get('params'):
                return response.data['params']
            
            # Return default params if none exist
            return {
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
            
        except Exception as e:
            logger.error(f"Error getting user params: {e}")
            return {}
    
    async def save_user_params(self, user_id: str, params: Dict) -> None:
        """Save user parameters to database."""
        try:
            # Upsert user with params
            response = self.client.table('users').upsert({
                'id': user_id,
                'params': params,
                'updated_at': datetime.now().isoformat()
            }).execute()
            
            logger.info(f"Saved params for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error saving user params: {e}")
            raise
    
    async def save_chat_message(
        self, 
        chat_id: str, 
        user_id: str, 
        message: str, 
        response: Dict
    ) -> None:
        """Save chat message and response to database."""
        try:
            # First, ensure chat exists
            chat_response = self.client.table('chats').select('id').eq('chat_id', chat_id).execute()
            
            if not chat_response.data:
                # Create new chat
                chat_title = self._generate_chat_title(message)
                self.client.table('chats').insert({
                    'chat_id': chat_id,
                    'user_id': user_id,
                    'title': chat_title,
                    'first_message': message,
                    'message_count': 1
                }).execute()
            else:
                # Update existing chat
                self.client.table('chats').update({
                    'updated_at': datetime.now().isoformat(),
                    'message_count': self.client.rpc('increment', {'x': 1, 'row_id': chat_response.data[0]['id']})
                }).eq('chat_id', chat_id).execute()
            
            # Save message
            self.client.table('messages').insert({
                'chat_id': chat_id,
                'user_id': user_id,
                'user_message': message,
                'ai_response': response
            }).execute()
            
            logger.info(f"Saved message for chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Error saving chat message: {e}")
            raise
    
    async def get_user_chats(self, user_id: str, start_date: str) -> List[Dict]:
        """Retrieve user's chat history from a specific date."""
        try:
            # Parse start date
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            
            # Query chats
            response = self.client.table('chats')\
                .select('chat_id, title, created_at, message_count')\
                .eq('user_id', user_id)\
                .gte('created_at', start_datetime.isoformat())\
                .order('created_at', desc=True)\
                .execute()
            
            if response.data:
                return [
                    {
                        'chat_id': chat['chat_id'],
                        'title': chat['title'] or 'Untitled Chat',
                        'created_at': datetime.fromisoformat(chat['created_at'].replace('Z', '+00:00')),
                        'message_count': chat['message_count']
                    }
                    for chat in response.data
                ]
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting user chats: {e}")
            return []
    
    async def get_chat_messages(self, chat_id: str) -> List[Dict]:
        """Get all messages for a specific chat."""
        try:
            response = self.client.table('messages')\
                .select('*')\
                .eq('chat_id', chat_id)\
                .order('created_at')\
                .execute()
            
            return response.data or []
            
        except Exception as e:
            logger.error(f"Error getting chat messages: {e}")
            return []
    
    async def delete_chat(self, chat_id: str, user_id: str) -> bool:
        """Delete a chat and all its messages."""
        try:
            # Verify ownership
            chat = self.client.table('chats')\
                .select('user_id')\
                .eq('chat_id', chat_id)\
                .single()\
                .execute()
            
            if chat.data and chat.data['user_id'] == user_id:
                # Delete chat (messages will cascade)
                self.client.table('chats').delete().eq('chat_id', chat_id).execute()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting chat: {e}")
            return False
    
    async def _create_anonymous_user(self) -> str:
        """Create an anonymous user for new sessions."""
        try:
            response = self.client.table('users').insert({
                'params': {
                    'persona': 'general',
                    'is_anonymous': True
                }
            }).execute()
            
            if response.data:
                return response.data[0]['id']
            
            raise Exception("Failed to create anonymous user")
            
        except Exception as e:
            logger.error(f"Error creating anonymous user: {e}")
            raise
    
    async def get_or_create_user(self, email: str = None) -> str:
        """Get existing user by email or create a new one."""
        try:
            if email:
                # Try to find existing user
                response = self.client.table('users').select('id').eq('email', email).execute()
                
                if response.data and len(response.data) > 0:
                    return response.data[0]['id']
                
                # Create new user with email
                response = self.client.table('users').insert({
                    'email': email,
                    'params': {
                        'persona': 'general',
                        'is_anonymous': False
                    }
                }).execute()
                
                if response.data:
                    return response.data[0]['id']
            else:
                # Create anonymous user
                return await self._create_anonymous_user()
                
        except Exception as e:
            logger.error(f"Error in get_or_create_user: {e}")
            raise
    
    def _generate_chat_title(self, first_message: str) -> str:
        """Generate a chat title from the first message."""
        if len(first_message) <= 50:
            return first_message
        
        title = first_message[:50]
        last_space = title.rfind(" ")
        if last_space > 30:
            title = title[:last_space]
        
        return title + "..."
    
    # Real-time subscriptions (Supabase feature)
    def subscribe_to_chat(self, chat_id: str, callback):
        """Subscribe to real-time updates for a chat."""
        channel = self.client.channel(f'chat_{chat_id}')
        
        channel.on(
            'postgres_changes',
            {
                'event': 'INSERT',
                'schema': 'public',
                'table': 'messages',
                'filter': f'chat_id=eq.{chat_id}'
            },
            callback
        ).subscribe()
        
        return channel

# Create global instance
db_service = SupabaseService()
