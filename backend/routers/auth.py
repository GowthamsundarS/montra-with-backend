from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, schemas, utils, oauth2

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(
    user_credentials: schemas.UserLogin,
    db: Session = Depends(database.get_db)
):

    # Find user by username
    user = db.query(models.user).filter(
        models.user.username == user_credentials.username
    ).first()

    # Check if user exists
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Verify password
    if not utils.verify(
        user_credentials.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create JWT Access Token
    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )

    # Return JWT Token
    return {
    "access_token": access_token,
    "token_type": "bearer",
    "username": user.username
}