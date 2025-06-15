# scripts/migrate_test_data.py - Migration script for test data

import asyncio
import os
import sys
from datetime import datetime, timedelta
import json
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.supabase_service import db_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_test_users():
    """Create test users for each persona"""
    test_users = [
        {
            "email": "zuri@example.com",
            "params": {
                "persona": "zuri",
                "sustainability_proficiency": "expert",
                "technological_proficiency": "advanced",
                "company_size": "Enterprise (10,000+ employees)",
                "industry": "Technology",
                "communication_style": "technical",
                "regulatory_importance": "critical",
                "budget_priority": "low"
            }
        },
        {
            "email": "amina@example.com",
            "params": {
                "persona": "amina",
                "sustainability_proficiency": "intermediate",
                "technological_proficiency": "beginner",
                "company_size": "Small (50-200 employees)",
                "industry": "Manufacturing",
                "communication_style": "business_focused",
                "regulatory_importance": "medium",
                "budget_priority": "high"
            }
        },
        {
            "email": "bjorn@example.com",
            "params": {
                "persona": "bjorn",
                "sustainability_proficiency": "advanced",
                "technological_proficiency": "intermediate",
                "company_size": "Large (500+ employees)",
                "industry": "Construction",
                "communication_style": "comprehensive",
                "regulatory_importance": "high",
                "budget_priority": "medium"
            }
        },
        {
            "email": "arjun@example.com",
            "params": {
                "persona": "arjun",
                "sustainability_proficiency": "intermediate",
                "technological_proficiency": "intermediate",
                "company_size": "Medium (80-300 employees)",
                "industry": "Retail",
                "communication_style": "simple_explanations",
                "regulatory_importance": "medium",
                "budget_priority": "medium"
            }
        }
    ]
    
    created_users = []
    for user_data in test_users:
        try:
            user_id = await db_service.get_or_create_user(user_data["email"])
            await db_service.save_user_params(str(user_id), user_data["params"])
            created_users.append((str(user_id), user_data["email"]))
            logger.info(f"Created/Updated user: {user_data['email']}")
        except Exception as e:
            logger.error(f"Error creating user {user_data['email']}: {e}")
    
    return created_users

async def create_test_chats(users):
    """Create test chat sessions with messages"""
    test_conversations = [
        {
            "user_email": "zuri@example.com",
            "chat_id": "zuri_chat_001",
            "messages": [
                {
                    "user": "We need to implement enterprise-wide sustainability reporting for our global operations. What solutions do you recommend?",
                    "ai": {
                        "response": "For enterprise-wide sustainability reporting across global operations, I recommend a comprehensive approach using Siemens solutions...",
                        "recommendations": [
                            {
                                "product_id": "sigreen",
                                "name": "SiGREEN",
                                "category": "Sustainability Management",
                                "description": "Comprehensive carbon footprint tracking and ESG reporting platform"
                            }
                        ],
                        "actions": [
                            {
                                "action_id": "explore_dbo_supply_chain",
                                "action_type": "select_dbo_scenario",
                                "action_label": "Explore Supply Chain Emission Transparency"
                            }
                        ]
                    }
                },
                {
                    "user": "How does SiGREEN integrate with our existing ERP systems?",
                    "ai": {
                        "response": "SiGREEN offers robust integration capabilities with major ERP systems including SAP, Oracle, and Microsoft Dynamics...",
                        "recommendations": [],
                        "actions": [
                            {
                                "action_id": "contact_expert",
                                "action_type": "contact_expert",
                                "action_label": "Connect with Integration Specialist"
                            }
                        ]
                    }
                }
            ]
        },
        {
            "user_email": "amina@example.com",
            "chat_id": "amina_chat_001",
            "messages": [
                {
                    "user": "I need cost-effective energy solutions for my manufacturing plant. What has the quickest ROI?",
                    "ai": {
                        "response": "For cost-effective energy solutions with quick ROI, I recommend starting with energy monitoring and LED lighting upgrades...",
                        "recommendations": [
                            {
                                "product_id": "building_x",
                                "name": "Building X",
                                "category": "Digital Building Platform",
                                "description": "Cloud-based building performance optimization"
                            }
                        ],
                        "dbo_suggestions": ["energy_optimization", "remote_energy_monitoring_for_smes"],
                        "actions": [
                            {
                                "action_id": "explore_energy_optimization",
                                "action_type": "select_dbo_scenario",
                                "action_label": "View Energy Optimization Details"
                            }
                        ]
                    }
                }
            ]
        }
    ]
    
    # Find user IDs
    user_map = {email: uid for uid, email in users}
    
    for conv in test_conversations:
        user_id = user_map.get(conv["user_email"])
        if not user_id:
            continue
            
        chat_id = conv["chat_id"]
        
        try:
            # Create chat messages
            for i, msg in enumerate(conv["messages"]):
                await db_service.save_chat_message(
                    chat_id=chat_id,
                    user_id=user_id,
                    message=msg["user"],
                    response=msg["ai"]
                )
                logger.info(f"Created message {i+1} for chat {chat_id}")
                
                # Add small delay to ensure proper ordering
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Error creating chat {chat_id}: {e}")

async def create_test_scenarios():
    """Ensure all DBO scenarios are properly loaded"""
    # This would typically sync with your dbo_scenarios.json
    logger.info("DBO scenarios should be loaded from dbo_scenarios.json on service startup")

async def verify_migration():
    """Verify the migration was successful"""
    logger.info("\n=== Verification ===")
    
    # Check users
    for email in ["zuri@example.com", "amina@example.com", "bjorn@example.com", "arjun@example.com"]:
        try:
            user_id = await db_service.get_user_id_from_chat(f"{email.split('@')[0]}_chat_001")
            params = await db_service.get_user_params(str(user_id))
            logger.info(f"✓ User {email}: {params.get('persona', 'unknown')} persona")
        except Exception as e:
            logger.error(f"✗ User {email}: {e}")
    
    # Check chats
    try:
        zuri_chats = await db_service.get_user_chats(
            user_map["zuri@example.com"],
            (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        )
        logger.info(f"✓ Found {len(zuri_chats)} chats for Zuri")
    except:
        logger.error("✗ Could not retrieve Zuri's chats")

async def main():
    """Run the migration"""
    logger.info("Starting test data migration...")
    
    try:
        # Create test users
        logger.info("\n1. Creating test users...")
        users = await create_test_users()
        
        # Create test chats
        logger.info("\n2. Creating test chats...")
        await create_test_chats(users)
        
        # Verify
        logger.info("\n3. Verifying migration...")
        global user_map
        user_map = {email: uid for uid, email in users}
        await verify_migration()
        
        logger.info("\n✅ Migration completed successfully!")
        
    except Exception as e:
        logger.error(f"\n❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())