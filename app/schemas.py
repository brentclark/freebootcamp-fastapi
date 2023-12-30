from pydantic import BaseModel, EmailStr, Field, ValidationError, validator
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """UserCreate"""

    email: EmailStr | None = Field(default=None)
    password: str
    created_at: Optional[datetime] = datetime.now()

    @validator("password", always=True)
    def validate_password1(cls, value: str):
        password = value
        min_length = 13
        errors = ""
        if len(password) < min_length:
            errors += f"Password must be at least {min_length} characters long. "
        if not any(character.islower() for character in password):
            errors += "Password should contain at least one lowercase character."
        if errors:
            raise ValueError(errors)

        return value

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """UserResponse"""

    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """UserLogin"""

    email: EmailStr
    password: str


class Post(BaseModel):
    """Post"""

    id: int
    title: str
    content: str
    published: Optional[bool] = True
    created_at: Optional[datetime] = datetime.now()
    user_id: Optional[int]
    user: Optional[UserResponse]


class PostCreate(Post):
    """PostCreate"""

    id: Optional[int]
    user_id: Optional[int]
    pass


class PostUpdate(Post):
    """PostUpdate"""

    pass


class PostCreateResponse(BaseModel):
    """PostCreateResponse"""

    title: str
    content: str
    # published: bool
    created_at: datetime
    id: int
    user_id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """TokenData"""

    id: int = None
    user_email: str = None
