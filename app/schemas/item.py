from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str
    price: float
    valute: Optional[str] = "Rubels"

class ItemCreate(ItemBase):
    media: Optional[str] = None

class ItemUpdate(BaseModel):


    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    valute: Optional[str] = None
    media: Optional[str] = None
    is_active: Optional[bool] = None

class ItemRead(ItemBase):

    id: int
    is_active: bool
    media: Optional[str] = None

    class Config:
        from_attributes = True