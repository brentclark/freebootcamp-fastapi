from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import (
    models,
    schemas,
    utils,
)
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[schemas.UserResponse])
def get_posts(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found"
        )
    return users


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Make sure email does not already exist
    check_user = db.query(models.User).filter(models.User.email == user.email).first()
    if check_user is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Email already exists"
        )

    create_user = models.User(**user.model_dump())
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    u = db.query(models.User).filter(models.User.id == id).first()

    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found"
        )

    return u
