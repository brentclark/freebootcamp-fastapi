from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy_utils import EmailType, PasswordType, force_auto_coercion
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import func

import enum
import random
import string

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )


force_auto_coercion()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    password = Column(
        PasswordType(
            schemes=["pbkdf2_sha512", "md5_crypt"],
            deprecated=["md5_crypt"],
            pbkdf2_sha512__rounds=600_000,
        ),
        unique=False,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # posts = relationship("Posts", back_populates="user", cascade="all, delete-orphan")

    # def verify_password(password, hashed_password) -> bool:
    #Verify the entered password against the hashed password
    # return pbkdf2_sha512.verify(password, hashed_password)


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(length=255), nullable=False)
    content = Column(String(255), nullable=False)
    published = Column(Boolean, server_default="1", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # user = relationship("User", back_populates="posts")
    user = relationship("User")
