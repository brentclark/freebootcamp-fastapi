from pydantic import BaseModel, EmailStr, Field, ValidationError, validator
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    created_at: Optional[datetime] = datetime.now()

class PostCreate(Post):
    pass

class PostUpdate(Post):
    pass

class PostCreateReponse(BaseModel):
    title: str
    content: str
    # published: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
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
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class User(UserResponse):

    class Config:
        orm_mode = True

