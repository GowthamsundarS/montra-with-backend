from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2

router = APIRouter(prefix="/expense", tags=["Expense"])


def _get_owned_expense_or_404(db: Session, id: int, user_id: int) -> models.Transaction:
    txn = db.query(models.Transaction).filter(
        models.Transaction.id == id,
        models.Transaction.user_id == user_id,
        models.Transaction.transaction_type == "expense",
    ).first()
    if txn is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"expense transaction with id: {id} was not found",
        )
    return txn


@router.post("/create_expense", response_model=schemas.ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    new_expense = models.Transaction(**expense.model_dump(), user_id=current_user.id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/get_expense", response_model=list[schemas.ExpenseResponse])
def get_expense_transactions(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.transaction_type == "expense",
    ).order_by(models.Transaction.date.desc()).offset(skip).limit(limit).all()


@router.put("/{id}", response_model=schemas.ExpenseResponse)
def update_expense(
    id: int,
    updated: schemas.TransactionUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    txn = _get_owned_expense_or_404(db, id, current_user.id)
    for field, value in updated.model_dump(exclude_unset=True).items():
        setattr(txn, field, value)
    db.commit()
    db.refresh(txn)
    return txn


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    txn = _get_owned_expense_or_404(db, id, current_user.id)
    db.delete(txn)
    db.commit()
