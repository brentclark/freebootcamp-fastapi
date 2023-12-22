from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException
from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine, select

class Posts(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

sqlite_file_name = "posts.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Check /redoc or /docs"}

# Get - All posts
@app.get("/posts/", response_model=List[Posts])
def read_all_posts():
    with Session(engine) as session:
        posts = session.exec(select(Posts)).all()
        return posts

# Get - A post
@app.get("/posts/{post_id}")
def read_a_post(post_id: int):
    with Session(engine) as session:
        statement = select(Posts).where(Posts.id == post_id)
        result = session.exec(statement)
        post = result.first() 
        return {
            "id": post
        }

# Post
@app.post("/posts/", response_model=Posts)
def create_post(post: Posts):
    print(post)
    with Session(engine) as session:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post