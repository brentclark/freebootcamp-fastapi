from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from typing import Any
from datetime import timedelta

router = APIRouter(prefix="/login", tags=["Authentication"])

@router.post("/", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
    response: Response = None,
) -> Any:
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify_password(user_credentials.password, user.password.hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(
        data={
            "user_email": user.email,
            "user_id": user.id,
        }
    )

    access_token_expires = timedelta(minutes=30)

    response.set_cookie(
        key="token",
        value=access_token,
        max_age=access_token_expires.total_seconds(),
        httponly=True,
    )

    return {"access_token": access_token, "token_type": "bearer"}