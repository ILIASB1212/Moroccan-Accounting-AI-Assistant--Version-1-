from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from .database import Base
from sqlalchemy.orm import  relationship
import datetime


class DBuser(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)
    messages = relationship("DBCHAT", back_populates="user", cascade="all, delete-orphan")




class DBCHAT(Base):
    __tablename__="chat"
    message_id = Column(Integer) # each message have unique id
    conversation_id=Column(String,primary_key=True,index=True) # each conversation/session have unique id 
    user_id = Column(Integer, ForeignKey("user.id")) # user id 
    role=Column(String)
    content=Column(String)
    timestamp=Column(DateTime,default=datetime.datetime.now())
    user = relationship("DBuser", back_populates="messages")

