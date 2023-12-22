from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine, select

class Posts(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool
    created_at: datetime = datetime.now

sqlite_file_name = "posts.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

app = FastAPI()

@app.get("/posts/")
def read_posts():
    with Session(engine) as session:
        posts = session.exec(select(Posts)).all()
        return posts
