from ..token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
# from datetime import timedelta
from .. import models
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, hashing, token
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication 🔑'])

get_db = database.get_db


@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')
    if not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect pasword')

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.username}
    )
    #, expires_delta=access_token_expires

    return {"access_token": access_token, "token_type": "bearer"}
