from sqlalchemy.orm import Session
from app.core.auth import get_hash
from app.models.user import User
from app.schemas.user import UserCreate
from datetime import datetime, timezone


def create_user(db: Session, obj_in: UserCreate):

    new_user = User(
        login=obj_in.login,
        hash_pass=get_hash(obj_in.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_by_login(db: Session, login: str):

    return db.query(User).filter(User.login == login).first()

def update_last_login(db: Session, obj_in: User):
    user = obj_in
    user.last_login = datetime.now(timezone.utc)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user