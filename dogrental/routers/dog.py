from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, schemas, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/dog',
    tags=['dogs 🐕']
)

get_db = database.get_db



@router.get('/')
def all_dog(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user) ):

    dogs = db.query(models.Dog).all()

    return dogs


@router.post('/')
def create_dog(request: schemas.Dog, db: Session = Depends(get_db)):
    
    newDog = models.Dog(name=request.name, race=request.race, tenant_id = 1)
    db.add(newDog)
    db.commit()
    db.refresh(newDog)

    return newDog

@router.get('/{id}')
def show_dog(id: int, db: Session = Depends(get_db)):

    dog = db.query(models.Dog).filter(models.Dog.id == id).first()

    if not dog:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"le chien {id} n'existe pas"
        )
    return dog

@router.delete('/{id}')
def delete_dog(id: int, db: Session = Depends(get_db)):

    dog = db.query(models.Dog).filter(models.Dog.id == id)

    if not dog.first():

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"le chien {id} n'existe pas"
        )
    dog.delete(synchronize_session=False)
    db.commit()

    return {'detail': 'deleted'}

@router.put('/{id}')
def update_dog(id: int,request: schemas.Dog, db: Session = Depends(get_db)):

    dog = db.query(models.Dog).filter(models.Dog.id == id)

    if not dog.first():

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"le chien {id} n'existe pas"
        )
    
    dog.update(request.dict())
    db.commit()

    return {'detail': 'updated'}
