from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, models, schemas, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/tenant',
    tags=['tenants 👤']
)

get_db = database.get_db



@router.get('/')
def all_tenant(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    tenants = db.query(models.Tenant).all()

    return tenants


@router.post('/')
def create_tenant(request: schemas.Tenant, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    newTenant = models.Tenant(firstname=request.firstname, lastname=request.lastname, email=request.email, adress=request.adress, user_id=1)
    db.add(newTenant)
    db.commit()
    db.refresh(newTenant)

    return newTenant

@router.get('/{id}')
def show_tenant(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    tenant = db.query(models.Tenant).filter(models.Tenant.id == id).first()

    if not tenant:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"le proprietaire {id} n'existe pas"
        )
    return tenant

@router.delete('/{id}')
def delete_tenant(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    tenant = db.query(models.Tenant).filter(models.Tenant.id == id)

    if not tenant.first():

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"le proprietaire {id} n'existe pas"
        )
    tenant.delete(synchronize_session=False)
    db.commit()

    return {'detail': 'deleted'}

@router.put('/{id}')
def update_tenant(id: int,request: schemas.Tenant, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    tenant = db.query(models.Tenant).filter(models.Tenant.id == id)

    if not tenant.first():

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"le proprietaire {id} n'existe pas"
        )
    
    tenant.update(request.dict())
    db.commit()

    return {'detail': 'updated'}
