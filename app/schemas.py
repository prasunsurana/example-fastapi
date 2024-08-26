from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

# Creating a blueprint for a post, pydantic BaseModel is a data validation subclass
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# Schema for user response
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# Schema for the database response. It inherits from PostBase, so it inherits the title, content and published
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    # This has to be added so that Pydantic can convert a SQLAlchemy model to a Pydantic model, just memorise
    class Config:
        orm_mode = True


class PostOut(PostBase):
    post: Post
    votes: int

    class Config:
        orm_mode = True


# Create a new user
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str 
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # imported from pydantic, less than or equal to 1, i.e. 0 or 1. 1 for like, 0 for 
    # un-like. However, also includes negatives numbers, dunno if there's another way?