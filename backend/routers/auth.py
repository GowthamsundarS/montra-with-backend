from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, schemas, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    # OAuth2PasswordRequestForm expects form fields "username" and "password".
    # This matches the tokenUrl="login" contract that OAuth2PasswordBearer
    # declares in oauth2.py, which is what lets Swagger UI's "Authorize"
    # button actually work against this endpoint.
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(
        models.User.username == user_credentials.username
    ).first()

    if user is None or not utils.verify(user_credentials.password, user.password):
        # Same error for "no such user" and "wrong password" — don't leak
        # which one it was.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
