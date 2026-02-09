# app/models/user.py
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, Boolean
from app.db.sessions import Base





class User(SQLAlchemyBaseUserTable[int], Base):

    __tablename__ = "users"

    #    email, hashed_password, is_active, is_superuser, is_verified
    # ID мы определяем сами, так как используем int (числа), а не UUID
    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, nullable=True)
    is_staff = Column(Boolean, default=False)