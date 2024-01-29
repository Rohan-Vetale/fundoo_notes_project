from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_NAME = getenv('DATABASE_NAME')
DATABASE_PASSWORD =getenv('DATABASE_PASSWORD')
DATABASE_DIALECT = getenv('DATABASE_DIALECT')
DATABASE_DRIVER = getenv('DATABASE_DRIVER')
DATABASE_USERNAME = getenv('DATABASE_USERNAME')
HOST = getenv('HOST')
DEFAULT_PORT = getenv('DEFAULT_PORT', default='5432')

