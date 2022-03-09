from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import Depends, HTTPException,Response, APIRouter
from typing import List, Optional

router=APIRouter(tags=['Posts'])


#GET ALL POSTS
@router.get('/posts')
def get_all(db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user),
            limit:int=10, skip:int=0, search:Optional[str]=""):
    post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

#CREATE POSTS
@router.post('/posts')
def create_post(post: schemas.Post,db:Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#GET ONE POST
@router.get('/posts/{id}')
def get_one(id:int, db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
    
#DELETE ONE POST
@router.delete('/posts/{id}')
def delete_post(id:int, db:Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    first_post=post_query.first()
    if not first_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if first_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

#UPDATE ONE POST
@router.put('/posts/{id}')
def update_post(id:int, updated_post:schemas.Post, db:Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    first_post=post_query.first()
    if not first_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if first_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()