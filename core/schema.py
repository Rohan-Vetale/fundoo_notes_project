"""
@Author: Rohan Vetale

@Date: 2024-01-28 19:44

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-01-28 19:24

@Title : Fundoo Notes schema module
"""
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr



class UserDetails(BaseModel):
    user_name: str = Field(default='Enter user name', title='Enter User name')
    password: str = Field(default='Enter user password', title='Enter User password', min_length=8)
    email: EmailStr = Field(default='Enter email id', title='Enter your email')
    first_name: str = Field(default='Enter First Name', title='Enter First Name', pattern=r"^[A-Z]{1}\D{3,}$")
    last_name: str = Field(default='Enter Last Name', title='Enter Last Name', pattern=r"^[A-Z]{1}\D{3,}$")
    state: str = Field(default='Enter your state Name', title='Enter your state Name')
    phone: int = Field(default='Enter phone number', title='Enter phone number')
    is_verified: Optional[bool] = Field(default=False)
    
class Userlogin(BaseModel):
    user_name: str = Field(default='Enter user name', title='Enter User name')
    password: str = Field(default='Enter user password', title='Enter User password')
    
class UserNotes(BaseModel):
    title: str = Field(default="Enter title of your note", pattern=r"^[A-Z]{1}\D{1,}")
    description: str
    color: str
    
class UserLabels(BaseModel):
    label_name : str = Field(default='Enter label name', title='Enter label name')
    
class CollaboratorSchema(BaseModel):
    note_id: int = Field(title='Enter note id')
    user_id: List[int]