from pydantic import BaseModel
from typing_extensions import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    email: str


class UserInResponse(BaseModel):
    id: int
    username: str
    email: str


class User(BaseModel):
    username: str
    email: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInLogin(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str = None
