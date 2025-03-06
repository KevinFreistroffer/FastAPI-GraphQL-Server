from sqlalchemy import Boolean, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column
from pydantic import Field
from sqlalchemy.dialects.postgresql import ARRAY  # For PostgreSQL arrays

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)
    fullname = mapped_column(String, nullable=True)

    def to_dict(self):
        return {
            column.name: getattr(self, column.name) 
            for column in self.__table__.columns
        }

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    
