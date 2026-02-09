from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Избегаем циклического импорта, используя manager и auth напрямую
from app.core.manager import get_user_manager
from app.core.auth import auth_backend
from fastapi_users import FastAPIUsers

from app.crud.item import get_item_by_id, update_item, delete_item, create_item
from app.db.sessions import get_async_session
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemRead, ItemUpdate, ItemCreate

# Инициализируем локальный объект для получения текущего пользователя
fastapi_users_tools = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users_tools.current_user(active=True)

router = APIRouter()


@router.get("/", response_model=List[ItemRead])
async def read_items(
        skip: int = 0,
        limit: int = 10,
        db :AsyncSession = Depends(get_async_session)
):
    query = select(Item).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{item_id}", response_model=ItemRead)
async def read_item(
        item_id: int,
        db: AsyncSession = Depends(get_async_session)
):
    return await get_item_by_id(db, id=item_id)


@router.post("/", response_model=ItemRead)
async def create_new_item(
        obj_in: ItemCreate,
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user)
):
    if not (user.is_staff or user.is_superuser):
        raise HTTPException(status_code = 403, detail="Forbidden")

    return await create_item(db, obj_in=obj_in)

@router.patch("/{item_id}", response_model=ItemRead)
async def patch_item(
        item_id: int,
        obj_in: ItemUpdate,
        db: AsyncSession = Depends(get_async_session),

        user: User = Depends(current_active_user)
):
    if not (user.is_staff or user.is_superuser):
        raise HTTPException(status_code = 403, detail="Forbidden")

    return await update_item(db,item_id=item_id, obj_in=obj_in)


@router.delete("/{item_id}", name="Deactivated Item")
async def remove_item(
    item_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):

    if not (user.is_staff or user.is_superuser):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = select(Item).where(Item.id == item_id)
    result = await db.execute(query)
    db_item = result.scalar_one_or_none()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")


    db_item.is_active = False
    await db.commit()
    return {"detail": "Item deactivated"}


@router.delete("/d/{item_id}", name="Delete Item")
async def remove_item(
        item_id: int,
        db: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_active_user)
):

    if not (user.is_staff or user.is_superuser):
        raise HTTPException(status_code=403, detail="Forbidden")

    return await delete_item(db=db, item_id=item_id)
