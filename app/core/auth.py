from fastapi import Depends
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy.db import DatabaseStrategy
# ВАЖНО: AccessTokenDatabase берется из адаптера БД
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase as AccessTokenDatabase

from app.core.config import settings
from app.models.access_token import AccessToken
from app.core.manager import get_access_token_db

bearer_transport = BearerTransport(tokenUrl="api/v1/auth/jwt/login")

def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=settings.EXPIRE_MIN * 60
    )

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)