from sqlalchemy import Boolean, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column
from pydantic import Field, BaseModel
from typing import Optional
from sqlalchemy.dialects.postgresql import ARRAY  # For PostgreSQL arrays

class AddressCreate(BaseModel):
    email_address: str = Field(alias="emailAddress")


class UserCreate(BaseModel):
    name: str
    fullname: Optional[str] = None
    # addresses: list[AddressSchema]

class UserUpdate(BaseModel):
    id: int
    name: Optional[str]
    fullname: Optional[str] = None