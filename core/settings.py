from dotenv import load_dotenv
import os

load_dotenv('.env')

DATABASE_NAME : str = os.getenv('DATABASE_NAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_DIALECT = os.getenv('DATABASE_DIALECT')
DATABASE_DRIVER = os.getenv('DATABASE_DRIVER')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
HOST = os.getenv('HOST')
DEFAULT_PORT = os.getenv('DEFAULT_PORT')
