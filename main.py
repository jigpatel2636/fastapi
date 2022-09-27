from cgitb import text
from typing import Optional
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

@app.get('/blog')
def index(limit=10, published : bool=True, sort: Optional[str]=None):
    if published:
        return {'data': f'{limit} published blog post'}
    else:
        return {'data': f'{limit} all blog post'}

@app.get('/data/unpublished')
def unpublished():
    return {"data": "Unpublished data is here"}

@app.get('blog/{id}')
def show(id):
    return {'data':id}

@app.get('blog/{id}/comments')
def show(id, limit=10):
    return {'data':{'1', '2'}}

class Blog(BaseModel):
    title: str
    body:str
    published_at: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f'Blog is created with {request.title}'}  