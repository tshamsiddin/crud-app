from .. import schemas, models, utils
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import Depends, HTTPException,Response, APIRouter

router=APIRouter(tags=['Users'])

@router.post('/users', status_code=201, response_model=schemas.UserResponse)
def create_user(user:schemas.User, db:Session=Depends(get_db)):
    h_password=utils.hash(user.password)
    user.password=h_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#GET USER INFO
@router.get('/users/{id}', response_model=schemas.UserResponse)
def get_user(id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Post not found")
    return user
