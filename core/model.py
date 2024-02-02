"""
@Author: Rohan Vetale

@Date: 2024-01-27 12:40

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-01-28 18:50

@Title : Fundoo Notes model module
"""

from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, String, create_engine, Text
from core.settings import DATABASE_DIALECT, DATABASE_DRIVER, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME, DEFAULT_PORT, HOST

database_url = f"{DATABASE_DIALECT}+{DATABASE_DRIVER}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{HOST}:{DEFAULT_PORT}/{DATABASE_NAME}"
engine = create_engine(database_url)
session = Session(engine)
Base = declarative_base()

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String(50), unique=True)
    phone = Column(BigInteger)
    state = Column(String(100))
    password = Column(String(100))
    is_verified = Column(Boolean, default=False)
    notes = relationship('Notes', back_populates='user')
    label = relationship('Labels', back_populates='user')
    
    def __repr__(self):
        return self.user_name
    
    
class Notes(Base):
    __tablename__ = 'notes'
    id = Column(BigInteger, index=True, primary_key=True, nullable=False)
    title = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=False )
    color = Column(String(20), nullable=False)
    reminder = Column(DateTime, default=None)
    user_id = Column(BigInteger, ForeignKey(column='user.id', ondelete='CASCADE'), nullable=False)
    user = relationship(argument='User', back_populates='notes')
    
    def __repr__(self):
        return str(self.id)

class Labels(Base):
    __tablename__ = 'label'

    id = Column(BigInteger, primary_key=True, index=True)
    label_name = Column(String(100))
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='label')

    def __repr__(self):
        return self.label_name  

    