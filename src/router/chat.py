from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.auth.oauth2 import get_current_user
from src.DataBase import db_chat
from src.DataBase.database import get_db
from .schema import MessageCreate, MessageResponse, ConversationResponse, UserAuth

router = APIRouter(tags=["chat"], prefix="/chat")

@router.post("/{user_id}/message")
def send_message(
    user_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)
):
    """Send a message in a conversation"""
    # Verify user exists
    user = db_chat.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # If no conversation_id provided, create new one
    conversation_id = message.conversation_id
    if not conversation_id:
        conversation_id = db_chat.create_conversation_id()
    
    # Save human message
    human_msg = db_chat.save_message(
        db=db,
        user_id=user_id,
        conversation_id=conversation_id,
        role="human",
        content=message.content
    )
    
    # TODO: Call your AI agent here
    ai_response = "This is a mock AI response"  # Replace with actual agent
    
    # Save AI response
    ai_msg = db_chat.save_message(
        db=db,
        user_id=user_id,
        conversation_id=conversation_id,
        role="ai",
        content=ai_response
    )
    
    return {
        "conversation_id": conversation_id,
        "human_message": human_msg,
        "ai_message": ai_msg
    }

@router.get("/{user_id}/conversations")
def get_user_conversations(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)
):
    """Get all conversations for a user"""
    return db_chat.get_user_conversations(db, user_id)

@router.get("/{user_id}/conversations/{conversation_id}")
def get_conversation(
    user_id: int,
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)
):
    """Get all messages in a conversation"""
    messages = db_chat.get_conversation(db, user_id, conversation_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return messages

@router.delete("/{user_id}/conversations/{conversation_id}")
def delete_conversation(
    user_id: int,
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)
):
    """Delete a conversation"""
    return db_chat.delete_conversation(db, user_id, conversation_id)