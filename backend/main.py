from fastapi import Body, FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Body, Depends
from pydantic import BaseModel
from . import utils
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .routers import auth
from .routers import user, income, expense
from .database import engine, SessionLocal
from .routers import user
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

import os
from fastapi.staticfiles import StaticFiles
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    conn = psycopg2.connect(host="localhost", database="from_scratch", user="postgres", password="root", cursor_factory=RealDictCursor)
    print("database connection was successfull")
except Exception as error:
    print("database connection failed")
    print("Error while connecting to PostgreSQL", error)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(income.router)
app.include_router(expense.router)

@app.get("/")
def root():
    return {"message": "Practicing to make a app backend with fastapi"}