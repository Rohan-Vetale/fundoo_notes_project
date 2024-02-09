from sqlalchemy.orm import Session, sessionmaker
from main import app
#test a real and genuine user registration 
def test_user_registration(client, user_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201
    # response_data = {'message': f"User Added successfully ", 'status': 201, 'data': data}
    # assert response.json() == response_data

#test a real and genuine user login
def test_login_user(client, user_data, login_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
