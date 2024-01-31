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
    
    
@router_notes.get(path='/get_all_notes/', status_code=status.HTTP_200_OK)
def read_notes(request: Request, db: Session = Depends(get_db)):
    """
    Description: This function is used to get all the notes titles of a user
    Parameter: response as Response object, db as database session.
    Return: Note titles of that user
    """
    try:
        notes_titles = db.query(Notes.title).filter_by(user_id=request.state.user.id).all()
        return{"message": f"All the notes title for {request.state.user.user_name} are : {notes_titles}"}
    except Exception as e:
        print(e)
        return{"message": str(e)}