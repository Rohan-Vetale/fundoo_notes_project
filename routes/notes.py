from core.utils import JWT, send_verification_mail
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, Request, status, Response, HTTPException
from sqlalchemy.orm import Session
from core.model import User, get_db, Notes
from core.schema import UserDetails, UserNotes, Userlogin
from passlib.hash import sha256_crypt

router_notes = APIRouter()


@router_notes.post(path='/add_notes', status_code=status.HTTP_201_CREATED)
def create_note(payload: UserNotes, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create fastapi for creating new note.
    Parameter: payload as NoteSchema object, response as Response object, db as database session.
    Return: Message of note added with status code 201.
    """
    print("this is add notes",request.state)
    try:
        print(request.state.user.id)
        body = payload.model_dump()
        body.update({'user_id': request.state.user.id})

        notes = Notes(**body)
        db.add(notes)
        db.commit()
        db.refresh(notes)
        return {'message': 'Note Added', 'status': 201, 'data': notes}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        print(e)
        return {"message": str(e)}