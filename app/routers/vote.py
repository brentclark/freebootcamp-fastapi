from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()

    if vote.direction == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {vote.post_id}",
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}

    if not found_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
        )

    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "successfully deleted vote"}
