from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import date
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    dob:date

class user_out(BaseModel):
    email: EmailStr
    username: str
    dob:date
    id: int
    profile_picture: Optional[str] = None
class UserLogin(BaseModel):
    username: str
    password: str
class transaction(BaseModel):
    name: str
    user_id: int
    amnt: int
    transaction_type: str
    category: str
    description: str
    date: date


class IncomeCreate(BaseModel):
    name: str
    amnt: int
    transaction_type: str = "income"
    category: str
    description: str
    date: date


class IncomeResponse(IncomeCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    name: str
    amnt: int
    transaction_type: str = "expense"
    category: str
    description: str
    date: date


class ExpenseResponse(ExpenseCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int