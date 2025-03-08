from sqlalchemy import Boolean, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import date

class ResetPasswordAttemptsSchema(BaseModel):
    timestamp: str

    class Config:
        from_attributes = True
        populate_by_name = True

class AvatarSchema(BaseModel):
    id: str # TODO: set it as ObjectID
    data: str
    content_type: str = Field(alias="contentType")
    
    class Config:
        from_attributes = True
        populate_by_name = True

class ReminderSchema(BaseModel):
    id: str  # TODO: set it as ObjectId
    custom_frequency: int = Field(alias="customFrequency")
    custom_unit: str = Field(alias="customUnit")
    date: str = Field(alias="date")
    description: str = Field(alias="description")
    end_date: str = Field(alias="endDate")
    ends: str = Field(alias="ends")
    occurrences: int = Field(alias="occurrences")
    recurrence_type: str = Field(alias="recurrenceType")
    recurring: bool = Field(alias="recurring")
    repeat_on: List[str] = Field(alias="repeatOn")
    time: str = Field(alias="time")
    title: str = Field(alias="title")

    class Config:
        from_attributes = True
        populate_by_name = True

class UserRole(str, Enum):
  ADMIN = "admin"
  MEMBER = "member"

class UserSchema(BaseModel):
    username: str
    username_normalized: str = Field(alias="usernameNormalized")
    email: str
    email_normalized: str = Field(alias="emailNormalized")
    password: str
    reset_password_token: str = Field(alias="resetPasswordToken")
    reset_password_token_expires: Optional[date] = Field(alias="resetPasswordTokenExpires")
    journals: List
    journal_categories: List = Field(alias="journalCategories")
    reset_password_attempts: List[ResetPasswordAttemptsSchema] = Field(alias="resetPasswordAttempts")
    is_verified: bool = Field(default=False, alias="isVerified")
    created_at: date = Field(alias="createdAt")
    updated_at: date = Field(alias="updatedAt")
    has_acknowledged_helper_text: bool = Field(alias="hasAcknowledgedHelperText")
    avatar: Optional[AvatarSchema]
    reminders: List[ReminderSchema]
    role: UserRole
    disabled: bool

    class Config:
        from_attributes = True
        populate_by_name = True
