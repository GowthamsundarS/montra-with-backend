from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, EmailStr
from datetime import date


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    dob: date


class UserOut(BaseModel):
    email: EmailStr
    username: str
    dob: date
    id: int
    profile_picture: Optional[str] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class TransactionBase(BaseModel):
    name: str
    amnt: Decimal
    category: str
    description: str
    date: date


class IncomeCreate(TransactionBase):
    transaction_type: str = "income"


class IncomeResponse(IncomeCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class ExpenseCreate(TransactionBase):
    transaction_type: str = "expense"


class ExpenseResponse(ExpenseCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class TransactionUpdate(BaseModel):
    name: Optional[str] = None
    amnt: Optional[Decimal] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
