from typing import Union
from fastapi import FastAPI
from schemas.Simple import UserCreate, UserUpdate
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker, Session
from models.db.User import DB_User, DB_Reminder, DB_Avatar
from models.db.Simple import Base, User
from sqlalchemy.orm import declarative_base
from operations.user import create_new_user, get_all_users, get_user_by_id, get_user_by_name, update_user


app = FastAPI(prefix="/api")

@app.post("/user/create")
def create_user(user: UserCreate):
    return create_new_user(user)

@app.get("/users")
def get_users():
    return get_all_users()

@app.get("/user/id/{id}")
def get_user_by_id(id: int):
    return get_user_by_id(id)

@app.get("/user/name/{name}")
def get_user_by_name(name: str):
    return get_user_by_name(name)

@app.put("/user")
def update_user(user: UserUpdate):
    return update_user(user)