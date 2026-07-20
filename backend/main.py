import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import models
from .database import engine
from .routers import user, auth, income, expense

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Montra API",
    description="Backend for Montra, a personal income/expense tracker.",
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(income.router)
app.include_router(expense.router)


@app.get("/")
def root():
    return {"message": "Montra API", "status": "ok", "docs": "/docs"}
