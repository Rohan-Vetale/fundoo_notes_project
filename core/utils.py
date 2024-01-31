
import pytz

from datetime import datetime, timedelta
from core.settings import SECRET_KEY, ALGORITHM, SENDER_EMAIL, SENDER_PASSWORD
from datetime import datetime, timedelta
import pytz
from jose import jwt
from fastapi import Depends, HTTPException, Request,status
from sqlalchemy.orm import Session
from core.model import get_db, User
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def jwt_authentication(request : Request,db:Session = Depends(get_db)):
    token = request.headers.get('authorization')
    decoded_token = JWT.jwt_decode(token)
    user_id = decoded_token.get('user_id')
    user_data = db.query(User).filter_by(id=user_id).one_or_none()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    request.state.user = user_data
    
    
    # user_data = db.query(User).filter_by(id=user_id).one_or_none
    # print(f"inside jwt authentication function {user_id}")
    # if user_data is None:
    #     raise HTTPException(detail='user not found',status_code=400)
    # request.state.user = user_data


# def jwt_authentication(request: Request, db: Session = Depends(get_db)):
#     token = request.headers.get('authorization')
#     decode_token = JWT.decode_data(token)
#     user_id = decode_token.get('user_id')
#     user = db.query(User).filter_by(id=user_id).one_or_none()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     request.state.user = user


class JWT:
    @staticmethod
    def jwt_encode(payload: dict):
        if 'exp' not in payload:
            payload.update(exp=datetime.now(pytz.utc) + timedelta(hours=1), iat=datetime.now(pytz.utc))
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def jwt_decode(token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.JWTError as e:
            print(e)
            
def send_verification_mail(verification_token : str, email):
    """
    Description:
    Function to send token link over provided email using smtp

    Parameter:
    verification_token : token generated while user login
    email : email of whom we want to send the link as a mail

    Return:
    None
    """
    try:
        # Your Gmail account details
        sender_email = SENDER_EMAIL
        sender_password = SENDER_PASSWORD
        recipient_email = email

        # Compose the email
        subject = 'Email Verification'
        body = f"Click the link to verify your email: http://127.0.0.1:8000/user/verify?token={verification_token}"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Set up the SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, recipient_email, msg.as_string())
        
        server.quit()
    except Exception as e:
        print(e)
        
    