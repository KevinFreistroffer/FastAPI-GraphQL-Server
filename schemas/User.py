from sqlalchemy import Boolean, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column
from pydantic import Field, BaseModel, EmailStr, validator
from typing import Optional
from sqlalchemy.dialects.postgresql import ARRAY  # For PostgreSQL arrays


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    name: Optional[str] = None
    # fullname: Optional[str] = None

    @validator('username')
    def username_validator(cls, v):
        if ' ' in v:
            raise ValueError("Username must not contain spaces")
        if len(v) < 5:
            raise ValueError("Username must be at least 5 characters")
        return v.lower()
    
    @validator('password')
    def password_validator(cls, v):
        if ' ' in v:
            raise ValueError("Password must not contain spaces")
        if len(v) < 5:
            raise ValueError("Password must be at least 5 characters")
        return v.lower()

    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Name",
                "username": "username",
                "email": "email@example.com",
                "password": "password"
            }
        }   
        

class UserUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    fullname: Optional[str] = None
    password: Optional[str] = None