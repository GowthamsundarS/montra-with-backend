from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2

router = APIRouter(
    prefix="/expense",
    tags=["Expense"]
)


@router.post("/create_expense", response_model=schemas.ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(database.get_db),
    current_user: models.user = Depends(oauth2.get_current_user)
):

    new_expense = models.Income_tab(
        **expense.model_dump(),
        user_id=current_user.id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/get_expense", response_model=list[schemas.ExpenseResponse])
def get_expense_transactions(
    db: Session = Depends(database.get_db),
    current_user: models.user = Depends(oauth2.get_current_user)
):

    transactions = db.query(models.Income_tab).filter(
        models.Income_tab.user_id == current_user.id,
        models.Income_tab.transaction_type == "expense"
    ).all()

    return transactions
