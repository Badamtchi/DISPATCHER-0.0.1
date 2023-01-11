from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List
import uuid
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/msg", tags=["Messages"])

@router.get("/inbox", response_model=List[schemas.MessageBack])
def get_msgs_inbox(db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    msgs = db.query(models.Messages).filter(models.Messages.receiver == user_id.phone).all()
    return msgs

@router.get("/unseen", response_model=List[schemas.MessageBack])
def get_msgs_unseen(db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    msgs = db.query(models.Messages).filter(models.Messages.receiver == user_id.phone, models.Messages.seen == False).all()
    return msgs

@router.get("/outbox", response_model=List[schemas.MessageBack])
def get_msgs_outbox(db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    msgs = db.query(models.Messages).filter(models.Messages.sender == user_id.phone).all()
    return msgs

@router.get("/{id}", response_model=schemas.MessageBack)
def get_msg(id: str, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    msg = db.query(models.Messages).filter(models.Messages.id == id).\
        filter(or_(models.Messages.sender == user_id.phone, models.Messages.receiver == user_id.phone)).first()
    if not msg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="message was not found!")
    return msg

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MessageBack)
def send_msg(msg: schemas.MessageCreate, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    new_id = uuid.uuid1()
    new_msg = models.Messages(id=new_id, sender=user_id.phone, **msg.dict())
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_msg(id: str, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    msg = db.query(models.Messages).filter(models.Messages.id == id).\
        filter(or_(models.Messages.sender == user_id.phone, models.Messages.receiver == user_id.phone))
    if not msg.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Message does not exist!")
    msg.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.MessageBack)
def edit_msg(id: str, updated_msg: schemas.MessageEdit, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    msg_query = db.query(models.Messages).filter(models.Messages.sender == user_id.phone, models.Messages.id == id)
    msg = msg_query.first()
    if msg == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
        detail="Message does not exist!")
    msg_query.update(updated_msg.dict(), synchronize_session=False)
    db.commit()
    return msg_query.first()