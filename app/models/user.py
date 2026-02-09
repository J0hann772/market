from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.sessions import Base



class User(SQLAlchemyBaseUserTable[int], Base):


    __tablename__ = "users"

    #    email, hashed_password, is_active, is_superuser, is_verified
    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, nullable=True)
    is_staff = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user")