from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2

router = APIRouter(prefix="/income", tags=["Income"])


def _get_owned_income_or_404(db: Session, id: int, user_id: int) -> models.Transaction:
    txn = db.query(models.Transaction).filter(
        models.Transaction.id == id,
        models.Transaction.user_id == user_id,
        models.Transaction.transaction_type == "income",
    ).first()
    if txn is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"income transaction with id: {id} was not found",
        )
    return txn


@router.post("/create_income", response_model=schemas.IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income(
    income: schemas.IncomeCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    new_income = models.Transaction(**income.model_dump(), user_id=current_user.id)
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income


@router.get("/get_income", response_model=list[schemas.IncomeResponse])
def get_income_transactions(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.transaction_type == "income",
    ).order_by(models.Transaction.date.desc()).offset(skip).limit(limit).all()


@router.put("/{id}", response_model=schemas.IncomeResponse)
def update_income(
    id: int,
    updated: schemas.TransactionUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    txn = _get_owned_income_or_404(db, id, current_user.id)
    for field, value in updated.model_dump(exclude_unset=True).items():
        setattr(txn, field, value)
    db.commit()
    db.refresh(txn)
    return txn


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    txn = _get_owned_income_or_404(db, id, current_user.id)
    db.delete(txn)
    db.commit()
