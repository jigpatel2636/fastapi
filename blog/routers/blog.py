from fastapi import APIRouter, Depends
from .. import schemas, database, models
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, status, Response, HTTPException

router = APIRouter()
get_db = database.get_db

@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(request: schemas.Blog, db:Session = Depends(get_db)):
     new_blog = models.Blog(title=request.title, body=request.body)
     db.add(new_blog)
     db.commit()
     db.refresh(new_blog)
     return new_blog

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id, db:Session = Depends(get_db) ):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not foudn')
    blog.delete(synchronize_session=False)
    db.commit()
    return "blog deleted"

@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemas.Blog, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not foudn')
    else:
        blog.update(request)
    db.commit()
    return "Blog is updated "

@router.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['blogs'])
def show_blog_byid(id, response: Response, db:Session = Depends(get_db) ):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detai": f"Blog with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog

@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all_blog(db:Session = Depends(get_db) ):
    blogs = db.query(models.Blog).all()
    if not blogs:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detai": f"Blog with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No blog is found")
    return blogs