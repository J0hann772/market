from typing import Optional
from fastapi import Request, Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase

from app.models.access_token import AccessToken
from app.models.user import User
from app.core.config import settings
from app.db.sessions import get_async_session
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY


    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # Здесь обычно пишут логику:
        # 1. Отправки приветственного письма (через Celery или SMTP).
        # 2. Логирования ("Пользователь id=5 зарегистрировался").
        # 3. Добавления приветственных бонусов.
        print(f"User {user.id} has registered.")

    # Также можно переопределить другие события:
    # async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
    #     print(f"User {user.id} forgot password. Token: {token}")

    # async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
    #     print(f"User {user.id} requested verification. Token: {token}")



async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)