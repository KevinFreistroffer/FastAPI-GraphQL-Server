from typing import Union
from fastapi import FastAPI
from schemas.Simple import UserCreate, UserUpdate
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker, Session
from models.db.User import DB_User, DB_Reminder, DB_Avatar
from models.db.Simple import Base, User
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={ "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(prefix="/api")

@app.post("/user/create")
def create_user(user: UserCreate):
    try:
        with Session(engine) as session:
            db_user = User(**user.model_dump())
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return user
    except Exception as e:
        print("error", e)
        return {}

@app.get("/users")
def get_users():
    try:
        with Session(engine) as session:
            stmt = select(User)
            print(stmt)
            result = session.scalars(stmt)
            users = [row.to_dict() for row in result]
            return { "users": users }
    except Exception as e:
        print(e)
        return []

@app.get("/user/id/{id}")
def get_user_by_id(id: int):
    print("get_user_by_id")
    try:
        with Session(engine) as session:
            stmt = select(User).where(User.id == id)
            result = session.scalars(stmt).one()
            if not result:
                return { "error": "User not found" }
            else:
                print("user found")

        return result.to_dict()
    except Exception as e:
        print(e)
        return {}

@app.get("/user/name/{name}")
def get_user_by_name(name: str):
    try:
        with Session(engine) as session:
            stmt = select(User).where(User.name == name)
            result = session.scalars(stmt)
            print(result)
            if not result:
                return { "error": "User not found" }
            
            return {
                "users": [ row.to_dict() for row in result]
            }
    except Exception as e:
        print(e)
        return { "error": f"An error occured {e}" }

@app.put("/user")
def update_user(user: UserUpdate):
    print(user)
    update(User).where(User.id == user.id)
    return {}