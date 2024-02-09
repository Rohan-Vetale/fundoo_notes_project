from sqlalchemy.orm import Session, sessionmaker
from main import app

#test user add notes genuine
def test_add_notes(client, user_data, login_data, notes_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header_token = response.json()['access_token']
    header = {'authorization': header_token}

    response = client.post('/notes/add_notes', headers=header, json=notes_data)
    assert response.status_code == 201

#test valid user get all notes
def test_get_all_notes(client, user_data, notes_data, login_data,new_notes_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200

    header = {'authorization': response.json()['access_token']}
    response = client.post('/notes/add_notes', json=notes_data, headers=header)
    assert response.status_code == 201

    response = client.post('/notes/add_notes',json=new_notes_data,headers=header)
    assert response.status_code == 201

    response = client.get('/notes/get_all_notes', headers=header)
    assert response.status_code == 200

#test valid user update notes
def test_update_notes(client,user_data,login_data,notes_data,update_notes_data,new_notes_data):
    response = client.post('/user/register',json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login',json=login_data)
    assert response.status_code == 200
    header = {'authorization':response.json()['access_token']}

    response = client.post('/notes/add_notes',json=notes_data,headers=header)
    assert response.status_code == 201

    response = client.post('/notes/add_notes',json=new_notes_data,headers=header)
    assert response.status_code == 201

    response = client.put('/notes/update_notes/1', headers=header,json=update_notes_data)
    assert response.status_code == 200



#test valid delete users
def test_del_user_note(client,user_data,login_data,notes_data,new_notes_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header = {'authorization': response.json()['access_token']}

    response = client.post('/notes/add_notes', json=notes_data, headers=header)
    assert response.status_code == 201

    response = client.post('/notes/add_notes', json=new_notes_data, headers=header)
    assert response.status_code == 201

    response = client.delete('/notes/delete/1', headers=header)
    assert response.status_code == 200
    
    
# test Attempt to create a note with invalid input data
def test_create_note_invalid_input(client, user_data, login_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    invalid_payload = {"title": "invalid Note", "description": None, "color": "yellow"}
    response = client.post("notes/add_notes", json=invalid_payload)
    assert response.status_code == 403

# test Attempt to create a note without providing required authentication token
def test_create_note_no_token(client, user_data, login_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header_token = response.json()['access_token']
    header = {'authorization': header_token}
    payload = {"title": "Test Note", "description": "This is a test note", "color": "blue"}
    response = client.post("notes/add_notes", json=payload)
    assert response.status_code == 403


