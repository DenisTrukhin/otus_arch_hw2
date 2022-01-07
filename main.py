import os
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import databases
import sqlalchemy


DATABASE_URL = os.environ.get('DATABASE_URL', '')


class User(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


app = FastAPI()
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("phone", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/user", response_model=User)
async def create_user(user: User):
    query = users.insert().values(
        username=user.username, first_name=user.first_name, last_name=user.last_name, email=user.email, phone=user.phone
    )
    new_user_id = await database.execute(query)
    return {"success": True, "id": new_user_id}


@app.get("/user/{user_id}", response_model=User)
async def get_user(user_id: int):
    query = users.select().where(users.columns.id == user_id)
    user = await database.fetch_one(query)
    return {"success": True, "user": user}


@app.put("/user/{user_id}")
async def update_user(user_id: int, user: Optional[User] = None):
    query = users.update().values(**user.dict()).where(users.columns.id == user_id)
    await database.execute(query)
    return {"success": True}


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.columns.id == user_id)
    await database.execute(query)
    return {"success": True}
