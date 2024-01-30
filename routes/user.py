"""
@Author: Rohan Vetale

@Date: 2024-01-28 12:40

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-01-28 19:23

@Title : Fundoo Notes user module
"""
from core.utils import JWT, send_verification_mail
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from core.model import User, get_db
from core.schema import UserDetails, Userlogin
from passlib.hash import sha256_crypt

router_user = APIRouter()
jwt_handler = JWT()


@router_user.post("/register", status_code=status.HTTP_201_CREATED)
def user_registration(body: UserDetails, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create api for adding a new user.
    Parameter: body as UserDetails object, response as Response object, db as database session.
    Return: Message of user data added with status code 201.
    """
    try:
        user_data = body.model_dump()
        user_data['password'] = sha256_crypt.hash(user_data['password'])
        new_user = User(**user_data)
        db.add(new_user)
        db.commit()
        token = jwt_handler.jwt_encode({'user_id': new_user.id})
        send_verification_mail(token, new_user.email)
        db.refresh(new_user)
        return {"status": 201, "message": "Registered successfully, check your mail to verify email", 'data': new_user, 'token' : token}
    except Exception as e:
        response.status_code = 400
        print(e)
        return {"message": str(e), 'status': 400}


@router_user.post("/login", status_code=status.HTTP_200_OK)
def user_login(payload: Userlogin, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function create api for login the user.
    Parameter: payload as Userlogin object, response as Response object, db as database session.
    Return: Message of user login with status code 201 and token generated by jwt header.
    """
    try:
        user = db.query(User).filter_by(user_name=payload.user_name).first()
        if user and sha256_crypt.verify(payload.password, user.password):
            return {'status': 200, "message": 'Logged in successfully'}
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message": 'Invalid username, password, or user not verified', 'status': 401}
    
    except Exception as e:
        response.status_code = 400
        return {"message": str(e), 'status': 400}
    
    
@router_user.get("/verify")
def verify_user(token: str, db: Session = Depends(get_db)):
    """
    Description: This function create api to verify the request when we click the verification link on send on mail.
    Parameter: token : object as string, db : as database session.
    Return: None
    """
    try:
        decode_token = JWT.jwt_decode(token)
        print(decode_token)
        user_id = decode_token.get('user_id')
        user = db.query(User).filter_by(id=user_id, is_verified=False).one_or_none()
        if not user:
            raise HTTPException(status_code=400, detail='User already verified or not found')
        user.is_verified = True
        db.commit()
        return {'status': 200, "message": 'User verified successfully', 'data': {}}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail='Internal Server Error')