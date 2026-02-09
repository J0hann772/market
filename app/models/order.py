from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship

from app.db.sessions import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    buy_at = Column(DateTime,default = lambda: datetime.now(timezone.utc))
    price_at_buy = Column(Float, nullable=False)
    status = Column(String, default="Not paid")

    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="orders")
    item = relationship("Item", back_populates="orders")

