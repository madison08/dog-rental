from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, schemas, hashing, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/user',
    tags=['users 👨']
)

get_db = database.get_db


@router.get('/')
def all_users(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    users = db.query(models.User).all()

    return users


@router.post('/')
def create_user(request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    hashedPassword = hashing.Hash.bcrypt(request.password)

    newUser = models.User(firstname=request.firstname, lastname=request.lastname, username=request.username, email=request.email, password = hashedPassword)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser

@router.get('/{id}')
def show_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"l'utilisateur {id} n'existe pas"
        )
    return user

@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"l'utilisateur {id} n'existe pas"
        )
    user.delete(synchronize_session=False)
    db.commit()

    return {'detail': 'deleted'}

@router.put('/{id}')
def update_user(id: int,request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"l'utilisateur {id} n'existe pas"
        )
    
    user.update(request.dict())
    db.commit()

    return {'detail': 'updated'}
