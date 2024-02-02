"""
@Author: Rohan Vetale

@Date: 2024-02-01 19:44

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-02-01 19:24

@Title : Fundoo Labels labels API
"""
from core.utils import JWT, send_verification_mail
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, Request, status, Response, HTTPException
from sqlalchemy.orm import Session
from core.model import Labels, User, get_db
from core.schema import  UserLabels

router_labels = APIRouter()


@router_labels.post(path='/add_label/', status_code=status.HTTP_201_CREATED)
def create_label(payload: UserLabels, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function is used for creating a new label and adding it
    Parameter: payload : UserLabels object, request : request state , db as database session, response : HttpResponse, db : DB object
    Return: Message of label added with status code 201
    """
    try:
        print(request.state.user.id)
        body = payload.model_dump()
        body.update({'user_id': request.state.user.id})

        labels_obj = Labels(**body)
        db.add(labels_obj)
        db.commit()
        db.refresh(labels_obj)
        return {'message': 'Label Added', 'status': 201, 'data': labels_obj}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        print(e)
        return {"message": str(e)}
    
    
@router_labels.get(path='/get_all_labels/', status_code=status.HTTP_200_OK)
def read_all_labels(request: Request, db: Session = Depends(get_db)):
    """
    Description: This function is used to get all the labels of a user
    Parameter: request : request state , db : database session
    Return: Label names of that user
    """
    try:
        label_names = db.query(Labels.label_name).filter_by(user_id=request.state.user.id).all()
        return{"message": f"All the label names for {request.state.user.user_name} are : {label_names}"}
    except Exception as e:
        return{"message": str(e)}
    
    
@router_labels.get(path='/view_full_label/{label_id}', status_code=status.HTTP_200_OK)
def view_full_Label(label_id : int, request: Request,response:Response, db: Session = Depends(get_db)):
    """
    Description: This function is used to get full label of a user
    Parameter: label_id: label number to fetch it, response : Response object, db : database session.
    Return: Complete label details
    """
    try:
        label_info = db.query(Labels).filter_by(user_id=request.state.user.id, id = label_id).one_or_none()
        #get the queried label object
        if label_info is None:
            raise HTTPException(detail= "Check the id provided and try again !",status_code=status.HTTP_404_NOT_FOUND)
        if label_info:
            label_id = f"Label id :  {label_info.id},  "
            label_name = f"Label Name :  {label_info.label_name},  "
            user_id = f"User ID :  {label_info.user_id}  "
            complete_info = label_id + label_name + user_id
            return{"message": f"Complete label info --> {complete_info}"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return{"message": "Check the label id and try again","status":400}
    
@router_labels.put(path="/update_labels/{label_id}", status_code=status.HTTP_200_OK)
def update_labels(label_id: int , change_Label: UserLabels, request: Request, response:Response, db: Session = Depends(get_db)):
    """
    Description: This function updates the user Label by Label id
    Parameter: label_id : id of the Label to be updated, request : request state , db as database session, response : HttpResponse, db : DB object
    Return: Message of Label updated with status code 200
    """
    try:
        queried_Label = db.query(Labels).filter_by(id=label_id, user_id = request.state.user.id).one_or_none()
        #get the queried Label object
        updated_Label = change_Label.model_dump()
        if queried_Label:
            [setattr(queried_Label, key, value) for key, value in updated_Label.items()]
            db.commit()
            db.refresh(queried_Label)
            return{"message":"Label updated succesfully !"}
        #incase of incorrect Label id return the status code 400 as bad request
        response.status_code = status.HTTP_400_BAD_REQUEST
        return{"message" : "Label cannot be updated"}
    except Exception as e:
        return{"message": f"Exception is {str(e)}"}
            
            
@router_labels.delete("/delete/{label_id}", status_code=status.HTTP_200_OK)
def delete_Label(label_id: int, request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function is used for deleting a Label from the table of Labels of a user
    Parameter: label_id : id of the Label to be deleted, status_code=status.HTTP_200_OK
    Return: Message of Label deleted with the status code 200 or 404 if Label not found
    """
    try:
        existing_Label = db.query(Labels).filter_by(user_id=request.state.user.id, id=label_id).one_or_none()
        #check and fetch for an existing Label
        if existing_Label:
            db.delete(existing_Label)
            db.commit()
            return {'message': 'Label Deleted', 'status': 200}
        raise HTTPException(detail='Label not found in the table database', status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        response.status_code = 400
        return {'message': str(e), 'status': 400}