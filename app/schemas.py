from pydantic import BaseModel ,EmailStr, constr, validator
from typing import Optional
from app.models import User

""" Authentication Schemas """
class LoginSchema(BaseModel):
    username: str
    password: str

""" User Schemas """
# class UserCreateSchema(BaseModel):
#     username: str
#     email: str
#     password: str

class UserCreateSchema(BaseModel):
    username: constr(min_length=4, max_length=50)  
    email: EmailStr 
    password: constr(min_length=8, max_length=50) 

    @validator('username')
    def validate_username(cls, value):
        if User.objects(username=value):
            raise ValueError('Username already exists')
        return value

    @validator('email')
    def validate_email(cls, value):
        if User.objects(email=value):
            raise ValueError('Email already exists')
        return value
    
    @validator('password')
    def password_complexity(cls, value):
        if not any(char.islower() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        return value

    class Config:
        extra = "forbid"

class UserGetSchema(BaseModel):
    name: str
    email: str

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

