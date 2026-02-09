from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship # <--- 1. Добавили импорт
from datetime import timezone, datetime
from app.db.sessions import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True, unique=True)
    description = Column(String)
    price = Column(Float, nullable=False)
    valute = Column(String, nullable=False, default="Rubles")
    media = Column(String)
    is_active = Column(Boolean, default=True)
    create_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    orders = relationship("Order", back_populates="item")