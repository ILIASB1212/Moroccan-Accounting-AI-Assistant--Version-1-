from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Message schemas
class Userbase(BaseModel):
    username:str
    email:str
    password:str

class UserDisplay(BaseModel):
    username:str
    email:str
    class Config():
        orm_mode=True


class MessageBase(BaseModel):
    content: str
    conversation_id: Optional[str] = None

class MessageCreate(MessageBase):
    pass

class MessageResponse(BaseModel):
    id: int
    user_id: int
    conversation_id: str
    role: str
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Conversation schemas
class ConversationResponse(BaseModel):
    conversation_id: str
    last_message: str
    last_timestamp: datetime
    message_count: int

# User auth schema (for dependency)
class UserAuth(BaseModel):
    id: int
    username: str
    email: str