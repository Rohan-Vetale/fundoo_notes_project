from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from main import app
from core.model import get_db, Base
from core.settings import DATABASE_DIALECT, DATABASE_DRIVER, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME, DEFAULT_PORT, HOST

database_url = f"{DATABASE_DIALECT}+{DATABASE_DRIVER}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{HOST}:{DEFAULT_PORT}/test_fundoo_notes"
engine = create_engine(database_url)
session = Session(engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    
@pytest.fixture
def user_data():
    return {
  "user_name": "rbv123455",
  "password": "rbv123455",
  "email": "vetalerohan@gmail.com",
  "first_name": "Rohan",
  "last_name": "Vetale",
  "state": "Maha",
  "phone": "8356853446",
  "is_verified": "true"
    }


@pytest.fixture
def login_data():
    return {
  "user_name": "rbv123455",
  "password": "rbv123455"
    }

@pytest.fixture
def notes_data():
    return {
        "title": "Pytest",
        "description": "using TestClient test the apis",
        "color": "red"
    }


@pytest.fixture
def new_notes_data():
    return {
        "title": "Override the get_db",
        "description": "for the api testing we are override the get_db function with override_get_db function",
        "color": "red"
    }

@pytest.fixture
def update_notes_data():
    return {
        "title": "Pytest",
        "description": "using TestClient test the apis",
        "color": "pink"
    }

@pytest.fixture
def label_data():
    return {
        'label_name': "python "
    }

@pytest.fixture
def update_label_data():
    return {
        'label_name': "python FastAPI "
    }
    
    
@pytest.fixture
def collab_detail():
    return {
            
    "note_id": 1,
    "user_id": [2]
    
    }

@pytest.fixture
def user2_data():
    return {
  "user_name": "rbv123456",
  "password": "rbv123456",
  "email": "vetalerohan2@gmail.com",
  "first_name": "RohanN",
  "last_name": "VetaleN",
  "state": "Maha",
  "phone": "8356853442",
  "is_verified": "true"
    }

