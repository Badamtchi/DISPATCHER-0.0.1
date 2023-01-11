from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBack)
def creat_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{phone}", response_model=schemas.UserBack)
def get_user(phone: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.phone == phone).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User does not exist!")
    return user