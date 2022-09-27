from fastapi import FastAPI
from blog.routers import user
from . import  models
from .database import engine, get_db
import blog
from .routers import blog
from .routers import user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)


