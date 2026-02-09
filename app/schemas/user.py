from fastapi_users import schemas



class UserRead(schemas.BaseUser[int]):
    username: str | None
    is_staff: bool


class UserCreate(schemas.BaseUserCreate):
    username: str | None



class UserUpdate(schemas.BaseUserUpdate):
    username: str | None



class UserAdminUpdate(schemas.BaseUserUpdate):
    username: str | None
    is_staff: bool | None
    is_active: bool | None
    is_superuser: bool | None