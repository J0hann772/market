from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.core.auth import auth_backend
from app.core.manager import get_user_manager
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate, UserCreate
from app.api.v1.endpoints.item import router as item_router

router = APIRouter()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router.include_router(
    item_router,
    prefix="/api/v1/items",
    tags=["items"],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/v1/auth/jwt",
    tags=["auth"],
)


router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/v1/auth",
    tags=["auth"],
)


router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/v1/users",
    tags=["users"],
)

