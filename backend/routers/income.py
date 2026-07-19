from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)


@router.post("/create_income", response_model=schemas.IncomeResponse, status_code=status.HTTP_201_CREATED)
def create_income(
    income: schemas.IncomeCreate,
    db: Session = Depends(database.get_db),
    current_user: models.user = Depends(oauth2.get_current_user)
):

    new_income = models.Income_tab(
        **income.model_dump(),
        user_id=current_user.id
    )

    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    return new_income
@router.get("/get_income", response_model=list[schemas.IncomeResponse])
def get_income_transactions(
    db: Session = Depends(database.get_db),
    current_user: models.user = Depends(oauth2.get_current_user)
):

    transactions = db.query(models.Income_tab).filter(
        models.Income_tab.user_id == current_user.id,
        models.Income_tab.transaction_type == "income"
    ).all()

    return transactions