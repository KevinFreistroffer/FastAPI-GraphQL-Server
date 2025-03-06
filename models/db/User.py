from sqlalchemy import Boolean, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column
from pydantic import Field
from sqlalchemy.dialects.postgresql import ARRAY  # For PostgreSQL arrays

class Base(DeclarativeBase):
    pass

class DB_User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String, unique=True, index=True)
    username_normalized = mapped_column(String)
    email = mapped_column(String, unique=True, index=True)
    email_normalized = mapped_column(String)
    password = mapped_column(String)
    reset_password_token = mapped_column(String)
    reset_password_token_expires = mapped_column(DateTime, nullable=True)
    is_verified = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime)
    updated_at = mapped_column(DateTime)
    has_acknowledged_helper_text = mapped_column(Boolean)
    role = mapped_column(String)
    disabled = mapped_column(Boolean)
    journals = mapped_column(ARRAY(String))
    journal_categories = mapped_column(ARRAY(String))
    reset_password_attempts = mapped_column(ARRAY(String))

    # Relationships
    reminders = relationship("DB_Reminder", back_populates="user")
    avatar = relationship("DB_Avatar", back_populates="user", uselist=False)

class DB_Reminder(Base):
    __tablename__ = "reminders"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    custom_frequency = mapped_column(Integer)
    custom_unit = mapped_column(String)
    date = mapped_column(String)
    description = mapped_column(String)
    end_date = mapped_column(String)
    ends = mapped_column(String)
    occurrences = mapped_column(Integer)
    recurrence_type = mapped_column(String)
    recurring = mapped_column(Boolean)
    repeat_on = mapped_column(ARRAY(String))  # PostgreSQL only
    time = mapped_column(String)
    title = mapped_column(String)

    parent_id = mapped_column(ForeignKey("DB_USER.id"))
    user = relationship("DB_User", back_populates="reminders")

class DB_Avatar(Base):
    __tablename__ = "avatars"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    data = mapped_column(String)
    content_type = mapped_column(String)

    # parent_id = mapped_column(ForeignKey("DB_USER.id"))
    user = relationship("DB_User", back_populates="avatar")