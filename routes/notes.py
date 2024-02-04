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
from core.model import User, get_db, Notes, collaborator
from core.schema import CollaboratorSchema, UserDetails, UserNotes, Userlogin
from passlib.hash import sha256_crypt

router_notes = APIRouter()


@router_notes.post(path='/add_notes', status_code=status.HTTP_201_CREATED, tags=["notes"])
def create_note(payload: UserNotes, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create fastapi for creating new note.
    Parameter: payload : UserNotes object, request : request state , db :database session, response : HttpResponse, db : DB object
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
    
    
@router_notes.get(path='/get_all_notes/', status_code=status.HTTP_200_OK, tags=["notes"])
def read_all_notes(request: Request, db: Session = Depends(get_db)):
    """
    Description: This function is used to get all the notes titles of a user
    Parameter: response : Response object, request : request state , db :database session, response : HttpResponse, db : DB object
    Return: Note titles of that user
    """
    try:
        existing_note = db.query(Notes).filter_by(user_id=request.state.user.id).all()
        collab_notes = db.query(collaborator).filter_by(user_id=request.state.user.id).all()
        notes = db.query(Notes).filter(Notes.id.in_(list(map(lambda x: x.note_id, collab_notes)))).all()
        existing_note.extend(notes)
        return {'message': 'Data retrieved', 'status': 200, 'data': existing_note}
    except Exception as e:
        return{"message": str(e)}
    

@router_notes.get(path='/view_full_note/{note_id}', status_code=status.HTTP_200_OK, tags=["notes"])
def view_full_note(note_id : int, request: Request,response:Response, db: Session = Depends(get_db)):
    """
    Description: This function is used to get all the notes titles of a user
    Parameter: response :Response object, db :database session.
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
    
@router_notes.put(path="/update_notes/{note_id}", status_code=status.HTTP_200_OK, tags=["notes"])
def update_notes(note_id: int , change_note: UserNotes, request: Request, response:Response, db: Session = Depends(get_db)):
    """
    Description: This function updates the user note by note id
    Parameter: note_id : id of the note to be updated, request : request state , db :database session, response : HttpResponse, db : DB object
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
            
            
@router_notes.delete("/delete/{note_id}", status_code=status.HTTP_200_OK, tags=["notes"])
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
    
    
@router_notes.post('/add_collaborator', status_code=status.HTTP_201_CREATED, tags=["notes"])
def add_collaborator(payload: CollaboratorSchema, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: Add a collaborator to a specific note.
    Parameter: payload :CollaboratorSchema object containing note_id and user_id,
               request :Request object, response :Response object, db :database session.
    Return: Message indicating the collaborator addition with status code 201.
    """
    try:
        # Query the note based on the provided note_id and user_id
        note = db.query(Notes).filter_by(user_id=request.state.user.id, id=payload.note_id).first()
        if not note:
            raise HTTPException(detail='Note not found', status_code=status.HTTP_404_NOT_FOUND)

        # Iterate through each collaborator_id in the payload
        for collaborator_id in payload.user_id:
            # Check if collaborator_id is not the same as the user_id making the request
            if collaborator_id != request.state.user.id:
                # Query the user based on collaborator_id
                body = db.query(User).filter_by(id=collaborator_id).first()
                if body:
                    # Check if the collaborator is not already added to the note and add if not present
                    if body not in note.user_m2m:
                        note.user_m2m.append(body)
                else:
                    raise HTTPException(detail=f'User with id {collaborator_id} not found',
                                        status_code=status.HTTP_404_NOT_FOUND)

        # Commit changes to the database
        db.commit()
        return {'message': 'Collaborators added to the note', 'status': 201}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(e), 'status': 400}


@router_notes.delete('/remove_collaborator', status_code=status.HTTP_200_OK, tags=["notes"])
def remove_collaborator(payload: CollaboratorSchema, request: Request, response: Response,
                        db: Session = Depends(get_db)):
    """
    Description: Remove a collaborator from a specific note.
    Parameter: payload :CollaboratorSchema object containing note_id and user_id,
               request :Request object, response :Response object, db :database session.
    Return: Message indicating the collaborator removal with status code 200.
    """
    try:
        # Query the note based on the provided note_id and user_id
        note = db.query(Notes).filter_by(user_id=request.state.user.id, id=payload.note_id).first()
        if not note:
            raise HTTPException(detail='Note not found', status_code=status.HTTP_404_NOT_FOUND)

        # Iterate through each collaborator_id in the payload
        for collaborator_id in payload.user_id:
            # Check if collaborator_id is not the same as the user_id making the request
            if collaborator_id != request.state.user.id:
                # Query the user based on collaborator_id
                body = db.query(User).filter_by(id=collaborator_id).first()
                if body:
                    # Check if the collaborator is in the note's collaborators list and remove if present
                    if body in note.user_m2m:
                        note.user_m2m.remove(body)
                else:
                    raise HTTPException(detail=f'User with id {collaborator_id} not found',
                                        status_code=status.HTTP_404_NOT_FOUND)

        # Commit changes to the database
        db.commit()
        return {'message': 'Collaborators removed from the note', 'status': 200}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(e), 'status': 400}
