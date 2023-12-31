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

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {post_id}, not found"
            )

        return {"id": post}


# Post
@app.post("/posts/", response_model=Posts, status_code=status.HTTP_201_CREATED)
def create_post(post: Posts):
    with Session(engine) as session:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post

# Update id
@app.patch("/posts/{post_id}", response_model=Posts)
def update_post(post_id: int, post: Posts):
    with Session(engine) as session:
        statement = select(Posts).where(Posts.id == post_id)
        result = session.exec(statement)
        update_post = result.first()

        if not update_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {post_id}, not found"
            )

        for key, value in post.model_dump(exclude_unset=True).items():
            setattr(update_post, key, value)

        session.add(update_post)
        session.commit()
        session.refresh(update_post)
        return update_post


# Delete - A post
@app.delete("/posts/{post_id}")
def delete_a_post(post_id: int):
    with Session(engine) as session:
        statement = select(Posts).where(Posts.id == post_id)
        result = session.exec(statement)
        post = result.first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {post_id}, not found"
            )

        session.delete(post)
        session.commit()
        return {"ok": True}
