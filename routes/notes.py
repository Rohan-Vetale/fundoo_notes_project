"""
@Author: Rohan Vetale

@Date: 2024-01-31 19:44

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-02-01 19:24

@Title : Fundoo Notes notes API
"""
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
    Parameter: payload : UserNotes object, request : request state , db as database session, response : HttpResponse, db : DB object
    Return: Message of note added with status code 201
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
def read_all_notes(request: Request, db: Session = Depends(get_db)):
    """
    Description: This function is used to get all the notes titles of a user
    Parameter: response : Response object, request : request state , db as database session, response : HttpResponse, db : DB object
    Return: Note titles of that user
    """
    try:
        notes_titles = db.query(Notes.title).filter_by(user_id=request.state.user.id).all()
        return{"message": f"All the notes title for {request.state.user.user_name} are : {notes_titles}"}
    except Exception as e:
        return{"message": str(e)}
    
    
@router_notes.get(path='/view_full_note/{note_id}', status_code=status.HTTP_200_OK)
def view_full_note(note_id : int, request: Request,response:Response, db: Session = Depends(get_db)):
    """
    Description: This function is used to get all the notes titles of a user
    Parameter: response as Response object, db as database session.
    Return: Note titles of that user
    """
    try:
        note_info = db.query(Notes).filter_by(user_id=request.state.user.id, id = note_id).one_or_none()
        #get the queried note object
        if note_info is None:
            raise HTTPException(detail= "Check the id provided and try again !",status_code=status.HTTP_404_NOT_FOUND)
        if note_info:
            note_title = f"Note title :  {note_info.title},  "
            note_description = f"Note description :  {note_info.description},  "
            note_color = f"Note color :  {note_info.color}  "
            complete_note = note_title + note_description + note_color
            return{"message": f"Complete note --> {complete_note}"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return{"message": "Check the note id and try again","status":400}
    
@router_notes.put(path="/update_notes/{note_id}", status_code=status.HTTP_200_OK)
def update_notes(note_id: int , change_note: UserNotes, request: Request, response:Response, db: Session = Depends(get_db)):
    """
    Description: This function updates the user note by note id
    Parameter: note_id : id of the note to be updated, request : request state , db as database session, response : HttpResponse, db : DB object
    Return: Message of note updated with status code 200
    """
    try:
        queried_note = db.query(Notes).filter_by(id=note_id, user_id = request.state.user.id).one_or_none()
        #get the queried note object
        updated_note = change_note.model_dump()
        if queried_note:
            [setattr(queried_note, key, value) for key, value in updated_note.items()]
            db.commit()
            db.refresh(queried_note)
            return{"message":"Note updated succesfully !"}
        #incase of incorrect note id return the status code 400 as bad request
        response.status_code = status.HTTP_400_BAD_REQUEST
        return{"message" : "Note cannot be updated"}
    except Exception as e:
        return{"message": f"Exception is {str(e)}"}
            
            
@router_notes.delete("/delete/{note_id}", status_code=status.HTTP_200_OK)
def delete_note(note_id: int, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function is used for deleting a note from the table of notes of a user
    Parameter: note_id : id of the note to be deleted, status_code=status.HTTP_200_OK
    Return: Message of note deleted with the status code 200 or 404 if note not found
    """
    try:
        existing_note = db.query(Notes).filter_by(user_id=request.state.user.id, id=note_id).one_or_none()
        #check and fetch for an existing note
        if existing_note:
            db.delete(existing_note)
            db.commit()
            return {'message': 'Note Deleted', 'status': 200}
        raise HTTPException(detail='Note not found in the table database', status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response.status_code = 400
        return {'message': str(e), 'status': 400}