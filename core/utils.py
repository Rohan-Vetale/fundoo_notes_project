
import pytz

from datetime import datetime, timedelta
from core.settings import HOST, REDIS_PORT, SECRET_KEY, ALGORITHM, SENDER_EMAIL, SENDER_PASSWORD, REDIS_URL
from datetime import datetime, timedelta
import pytz
from jose import jwt
from fastapi import Depends, HTTPException, Request,status
from sqlalchemy.orm import Session
from core.model import get_db, User, RequestLog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import redis
from task import celery
redis_obj = redis.Redis(host=HOST, port=REDIS_PORT, decode_responses=True)


def jwt_authentication(request : Request, db:Session = Depends(get_db)):
    try:
        token = request.headers.get('authorization')
        decoded_token = JWT.jwt_decode(token)
        user_id = decoded_token.get('user_id')
        user_data = db.query(User).filter_by(id=user_id).one_or_none()
        if not user_data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        request.state.user = user_data
    except Exception as e:
        print(e)
    
    
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
    
@celery.task        
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
        
class Redis:
    @staticmethod
    def add_redis(name, key, value):
        """
        Description: This function add and update data in redis memory.
        Parameter: name: key, key: field ,  value: value as parameter.
        Return: set the name, key, value to redis memory
        """
        return redis_obj.hset(name, key, value)

    @staticmethod
    def get_redis(name):
        """
        Description: This function get all data from redis memory.
        Parameter: name as parameter.
        Return: get all data from the redis memory using name.
        """
        return redis_obj.hgetall(name)

    @staticmethod
    def delete_redis(name, key):
        """
        Description: This function delete data from redis memory.
        Parameter: name, key as parameter.
        Return: delete data from redis using name and list of key.
        """
        return redis_obj.hdel(name, key)
    
def request_loger(request):
    """
    Description: This function update the middleware table in database.
    Parameter: request as parameter.
    Return: None
    """
    session = get_db()
    db = next(session)
    #db:Session = Depends(get_db)
    log = db.query(RequestLog).filter_by(request_method=request.method,
                                         request_path=request.url.path).one_or_none()
    if not log:
        #if the row does not exist then create it and make count 1
        log = RequestLog(request_method=request.method, request_path=request.url.path, count=1)
        db.add(log)
    else:
        #if the row exists then make the count = count +1
        log.count += 1

    db.commit()