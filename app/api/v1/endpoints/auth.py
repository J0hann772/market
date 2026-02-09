from datetime import datetime, timezone


from fastapi import Depends, HTTPException, FastAPI, APIRouter
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.auth import verify_pass, create_token
from app.crud.user import get_by_login, create_user, update_last_login
from app.schemas.user import UserCreate, UserOut

router = APIRouter()

@router.post('/register', response_model=UserOut)
def register(obj_in: UserCreate, db: Session = Depends(get_db)):
    user = get_by_login(db=db, login=obj_in.login)

    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = create_user(db, obj_in)
    access_token = create_token(data={"sub": new_user.login})

    return {
        "id": new_user.id,
        "login": new_user.login,
        "is_staff": new_user.is_staff,
        "access_token": access_token
    }


@router.post('/login', response_model=UserOut)
def login(obj_in: UserCreate, db: Session = Depends(get_db)):
    user = get_by_login(db=db, login=obj_in.login)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    if not user or not verify_pass(obj_in.password, user.hash_pass):
        raise HTTPException(status_code=400, detail="Wrong password")

    update_last_login(db, user)
    access_token = create_token(data={"sub":user.login})

    return {
        "id": user.id,
        "login": user.login,
        "is_staff": user.is_staff,
        "access_token": access_token
    }
