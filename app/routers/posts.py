from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, mapper
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/")
# @router.get("/", response_model=List[schemas.P])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Posts, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True)
        .group_by(models.Posts.id)
        .filter(models.Posts.title.contains(search))
        .limit(limit=limit)
        .offset(skip)
        .all()
    )

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No posts found"
        )

    # if posts.user_id != current_user.id:
    # raise HTTPException(
    # status_code=status.HTTP_403_FORBIDDEN, detail="User not authorised to view posts"
    # )

    return posts


@router.get("/{post_id}", response_model=schemas.PostOut)
def read_a_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    post = (
        db.query(models.Posts, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True)
        .group_by(models.Posts.id)
        .filter(models.Posts.id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {post_id}, not found"
        )

    # if post.user_id != current_user.id:
    # raise HTTPException(
    # status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorised to view post {id}"
    # )

    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostCreateResponse,
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    create_post = models.Posts(**post.model_dump())
    setattr(create_post, "user_id", current_user.id)

    db.add(create_post)
    db.commit()
    db.refresh(create_post)
    return create_post


@router.patch("/{post_id}", response_model=schemas.Post)
def update_post(
    post_id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    update_post = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    if update_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {post_id}, not found"
        )

    if update_post.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User not authorised to update post {update_post.id}",
        )

    for key, value in post.model_dump(exclude_unset=True).items():
        setattr(update_post, key, value)

    db.add(update_post)
    db.commit()
    db.refresh(update_post)
    return update_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    delete_post = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    if not delete_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {post_id}, not found"
        )

    # Iterate over the attributes of the object and print their names and values
    # mapper = object_mapper(delete_post)
    # for column in mapper.columns:
    # attribute_name = column.key
    # attribute_value = getattr(delete_post, attribute_name)
    # print(f"{attribute_name}: {attribute_value}")

    if delete_post.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User not authorised to delete post {delete_post.id}",
        )

    db.delete(delete_post)
    db.commit()
