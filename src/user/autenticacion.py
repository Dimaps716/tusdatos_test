import hashlib
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.params import Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from db import buscar_usuario_email_or_username
from src.models.user import Token, UserInDB, UserInLogin

from settings import Settings

settings = Settings()


class AuthHandler:
    def __init__(self):
        pass

    def verify_password(self, plain_password, hashed_password):
        hashed_plain_password = hashlib.sha256(plain_password.encode()).hexdigest()
        return hashed_plain_password == hashed_password

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user["password"]):
            return False
        return user

    def get_user(self, username: str):
        user_dict = buscar_usuario_email_or_username(username=username)
        if user_dict and username in user_dict.get("username", []):
            return user_dict

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    def is_token_valid(self, token):
        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            expiration_time = decoded_token.get("exp")

            return expiration_time > datetime.utcnow().timestamp()
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")


auth_handler = AuthHandler()


def create_access_token(data: dict):
    return auth_handler.create_access_token(data)


def validate_token(token: str = Header(...)):
    return auth_handler.is_token_valid(token)
