from fastapi import APIRouter,Depends
from src.DataBase import db_user
from src.DataBase.database import get_db
from .schema import Userbase,UserDisplay
from sqlalchemy.orm.session import Session
router=APIRouter(tags=["user"],prefix="/user")

@router.post("/create",response_model=UserDisplay)
def add_user(request:Userbase,db:Session=Depends(get_db)):
    return db_user.create_user(db,request)