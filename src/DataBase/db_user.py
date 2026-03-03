from fastapi import HTTPException ,status
from src.router.schema import Userbase
from sqlalchemy.orm.session import Session
from .models import DBuser
from .hash import Hash


def create_user(db:Session,request:Userbase):
    new_user=DBuser(username=request.username,
                    email=request.email,
                    password=Hash.encode(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db:Session,username:str):
    user=db.query(DBuser).filter(DBuser.username==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with username : {username} not found ")
    return user