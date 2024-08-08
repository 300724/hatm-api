from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from auth.models import User as UserModel
from auth.schemas import TokenData
from config import ALGORITHM, SECRET_KEY
from database import get_db
from logger import LOGGER

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# todo: do we need it? pylint: disable=W0511
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(user_id: str):
    try:
        db = next(get_db())
        return db.query(UserModel).filter(UserModel.user_id == user_id).first()
    except Exception as e:
        LOGGER.error(e)
        return None


def authenticate_user(user_id: str):
    user = get_user(pwd_context.hash(user_id))
    if not user:
        return False
    return user


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_data = TokenData(user_id=user_id)
        user = get_user(user_id=token_data.user_id)
        return user
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
