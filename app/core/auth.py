from fastapi import Depends
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.authentication.strategy.db import DatabaseStrategy
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase as AccessTokenDatabase

from app.core.config import settings
from app.models.access_token import AccessToken
from app.core.manager import get_access_token_db


cookie_transport = CookieTransport(
    cookie_name="market_auth",
    cookie_max_age=settings.EXPIRE_MIN * 60,
    cookie_httponly=True,
    cookie_samesite="lax"
)

def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=settings.EXPIRE_MIN * 60
    )

auth_backend = AuthenticationBackend(
    name="jwt_cookie",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)