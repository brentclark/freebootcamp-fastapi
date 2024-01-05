from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy_utils import EmailType, PasswordType
from sqlalchemy.orm import relationship
from .database import Base
from .schemas import PasswordType
from sqlalchemy.sql import func

import enum
import random
import string
import hashlib


def random_password_type() -> PasswordType:
    return random.choice([PasswordType.MD5, PasswordType.SHA256, PasswordType.SHA1])


def random_salt() -> str:
    return "".join(random.choice(string.ascii_letters) for i in range(10))


def encrypt_password(ptype: PasswordType, salt: str, plain: str):
    password = "{}*{}^".format(salt, plain)
    m = hashlib.md5()
    if ptype == PasswordType.SHA256:
        m = hashlib.sha256()
        m = hashlib.sha1()
    m.update(password.encode())
    return m.hexdigest()


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


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    salt = Column(String, nullable=False, default="")
    password = Column(String, nullable=False, default="")
    ptype = Column(Enum(PasswordType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # posts = relationship("Posts", back_populates="user", cascade="all, delete-orphan")

    def check_password(self, plain: str) -> bool:
        return self.password and encrypt_password(self.ptype, self.salt, plain) == self.password


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # user = relationship("User", back_populates="posts")
    user = relationship("User")
