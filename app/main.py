from fastapi import FastAPI
from .database import engine, get_db
from . import models
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="FastAPI Post Backend - By Brent Clark")

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
