from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class User(BaseModel):
    user_id: str
    is_admin: bool
    is_superuser: bool


@dataclass(frozen=True)
class Token(BaseModel):
    access_token: str
    access_token_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int


@dataclass(frozen=True)
class TokenData(BaseModel):
    user_id: str


@dataclass(frozen=True)
class RefreshTokenDto(BaseModel):
    refresh_token: str


class UserCredentialsDto(BaseModel):
    client_id: str
    password: str


class UserTokensDto(BaseModel):
    access_token: str
    refresh_token: str
