from  fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.DataBase.database import get_db
from src.DataBase.models import DBuser
from src.DataBase.hash import Hash
from .oauth2 import create_access_token
router=APIRouter(tags=["authontification"])

@router.post("/login")
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(DBuser).filter(DBuser.username==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"wrong username or not found ")
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"wrong password ")
    
    access_token=create_access_token({"username":user.username})
    return {"access_token":access_token,
            "algorithme":"ssl",
             "username":user.username,
              "user_id":user.id,}
    
