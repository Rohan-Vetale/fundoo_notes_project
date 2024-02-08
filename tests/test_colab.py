from sqlalchemy.orm import Session, sessionmaker
from main import app

def test_add_colaborator(client,user_data,login_data,notes_data,new_notes_data,collab_detail,user2_data):
    response = client.post('/user/register',json=user_data)
    assert response.status_code == 201
    
    response = client.post('/user/register',json=user2_data)
    assert response.status_code == 201

    response = client.post('/user/login',json=login_data)
    assert response.status_code == 200
    header = {'authorization':response.json()['access_token']}

    response = client.post('/notes/add_notes',json=notes_data,headers=header)
    assert response.status_code == 201

    response = client.post('/notes/add_notes',json=new_notes_data,headers=header)
    assert response.status_code == 201
    
    response = client.post('/notes/add_collaborator',payload = collab_detail, headers=header )

    