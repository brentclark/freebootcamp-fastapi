from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db
from .schemas import Post, PostCreate, PostUpdate, PostCreateReponse

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts found"
        )
    return posts


@app.get("/posts/{post_id}", response_model=Post)
def read_a_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {post_id}, not found"
        )

    return post


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=PostCreateReponse
)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    create_post = models.Posts(**post.model_dump())
    db.add(create_post)
    db.commit()
    db.refresh(create_post)
    return create_post


@app.patch("/posts/{post_id}", response_model=Post)
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    update_post = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    if update_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {post_id}, not found"
        )

    for key, value in post.model_dump(exclude_unset=True).items():
        setattr(update_post, key, value)

    db.add(update_post)
    db.commit()
    db.refresh(update_post)
    return update_post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    delete_post = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    if not delete_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {post_id}, not found"
        )

    db.delete(delete_post)
    db.commit()
