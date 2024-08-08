from typing import Annotated, Union

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    is_admin: bool
    is_superuser: bool


class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    is_admin: bool
    is_superuser: bool


class Token(BaseModel):
    access_token: str
    access_token_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int


class TokenData(BaseModel):
    username: str


class AuthPassword(BaseModel):
    username: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str
