import os
import time

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2, utils
from ..database import get_db

router = APIRouter(tags=["Users"])

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        (models.User.email == new_user.email) | (models.User.username == new_user.username)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email or username already exists",
        )

    user_data = new_user.model_dump()
    user_data["password"] = utils.hash_password(user_data["password"])

    user = models.User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )
    return user


@router.get("/user/profile", response_model=schemas.UserOut)
def get_user_profile(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user


@router.post("/user/upload-profile")
async def upload_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only jpg, jpeg, png, and webp are allowed.",
        )

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large. Maximum size allowed is 5 MB.",
        )

    os.makedirs("uploads", exist_ok=True)

    if current_user.profile_picture and os.path.isfile(current_user.profile_picture):
        try:
            os.remove(current_user.profile_picture)
        except OSError as e:
            print(f"Error removing old profile picture: {e}")

    filename = f"profile_{current_user.id}_{int(time.time())}.{file_ext}"
    relative_path = f"uploads/{filename}"

    try:
        with open(relative_path, "wb") as f:
            f.write(contents)
    except OSError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save profile picture.",
        )

    current_user.profile_picture = relative_path
    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile picture updated",
        "profile_picture": relative_path,
    }
