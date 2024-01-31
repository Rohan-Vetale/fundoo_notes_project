from core.utils import JWT, send_verification_mail
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from core.model import User, get_db, Notes
from core.schema import UserDetails, Userlogin
from passlib.hash import sha256_crypt

router_notes = APIRouter


@router_notes.post(path="/add_note",status_code=status.HTTP_201_CREATED)
def add_notes(payload: Notes, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function is used to create notes 
    Parameter: payload: Notes details, response as Response object, db as database session.
    Return: Message of user notes added with status code 201
    """
    note = payload.model_dump()
    new_note = Notes(**note)
    db.add(new_note)
    db.commit()