from sqlalchemy.orm import Session
from src.DataBase.models import DBCHAT, DBuser
from datetime import datetime
from typing import List, Optional
import uuid

# ===== MESSAGE OPERATIONS =====

def create_conversation_id() -> str:
    """Generate a unique conversation ID"""
    return str(uuid.uuid4())

def save_message(db: Session, user_id: int, conversation_id: str, role: str, content: str):
    """Save a single message"""
    db_message = DBCHAT(
        user_id=user_id,
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_user_messages(db: Session, user_id: int):
    """Get all messages for a user"""
    return db.query(DBCHAT).filter(DBCHAT.user_id == user_id).order_by(DBCHAT.timestamp).all()

def get_user_conversations(db: Session, user_id: int):
    """Get all unique conversation IDs for a user with last message preview"""
    # Get all messages for user
    messages = db.query(DBCHAT).filter(DBCHAT.user_id == user_id).order_by(DBCHAT.timestamp).all()
    
    # Group by conversation_id
    conversations = {}
    for msg in messages:
        if msg.conversation_id not in conversations:
            conversations[msg.conversation_id] = {
                "conversation_id": msg.conversation_id,
                "last_message": msg.content[:100] + "..." if len(msg.content) > 100 else msg.content,
                "last_timestamp": msg.timestamp,
                "message_count": 0
            }
        conversations[msg.conversation_id]["message_count"] += 1
    
    return list(conversations.values())

def get_conversation(db: Session, user_id: int, conversation_id: str):
    """Get all messages in a specific conversation"""
    return db.query(DBCHAT)\
        .filter(DBCHAT.user_id == user_id)\
        .filter(DBCHAT.conversation_id == conversation_id)\
        .order_by(DBCHAT.timestamp)\
        .all()

def delete_conversation(db: Session, user_id: int, conversation_id: str):
    """Delete an entire conversation"""
    db.query(DBCHAT)\
        .filter(DBCHAT.user_id == user_id)\
        .filter(DBCHAT.conversation_id == conversation_id)\
        .delete(synchronize_session=False)
    db.commit()
    return {"message": "Conversation deleted"}

# ===== USER OPERATIONS =====

def get_user_by_id(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(DBuser).filter(DBuser.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Get user by username"""
    return db.query(DBuser).filter(DBuser.username == username).first()