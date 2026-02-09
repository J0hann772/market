from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    status: Optional[str] = "Not paid"

class OrderRead(OrderBase):
    id: int
    item_id: int
    user_id: int
    price_at_buy: float
    buy_at: datetime

    class Config:
        from_attributes = True



class OrderCreate(OrderBase):
    item_id: int


class OrderUpdate(OrderBase):
    status: Optional[str] = None


