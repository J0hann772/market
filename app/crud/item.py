from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate






async def create_item(db: AsyncSession, obj_in: ItemCreate):

    query = select(Item).where(Item.title == obj_in.title)
    result = await db.execute(query)
    existing_item = result.scalar_one_or_none()

    if existing_item:
        raise HTTPException(status_code=400, detail="The item already exists")

    new_item = Item(**obj_in.model_dump())

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    return new_item

async def get_item_by_id(db: AsyncSession, id: int):

    query = select(Item).where(Item.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()


    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item



async def update_item(db: AsyncSession, item_id: int, obj_in: ItemUpdate):

    query = select(Item).where(Item.id == item_id)
    result = await db.execute(query)
    db_item = result.scalar_one_or_none()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")



    update_data = obj_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    return db_item


async def delete_item(db: AsyncSession, item_id: int):
    query = select(Item).where(Item.id == item_id)
    result = await db.execute(query)
    db_item = result.scalar_one_or_none()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(db_item)
    await db.commit()
    return {"detail": "Item deleted"}


