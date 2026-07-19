
 
from .. import models,schemas,oauth2
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter, UploadFile, File
from .. import utils
from .. database import engine,SessionLocal,get_db
import os
import time

from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/users",status_code=status.HTTP_201_CREATED)
def users(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hashing the password
    hashed_password=utils.pwd_context.hash(new_user.password)
    new_user.password = hashed_password
    user1 = models.user(**new_user.dict())
    db.add(user1)
    db.commit()
    db.refresh(user1)
    return user1

@router.get("/users/{id}",response_model=schemas.user_out)
def get_user(id:int,db: Session = Depends(get_db)):
    user =db.query(models.user).filter(models.user.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} was not found")
    return user

@router.get("/user/profile", response_model=schemas.user_out)
def get_user_profile(current_user: models.user = Depends(oauth2.get_current_user)):
    return current_user

@router.post("/user/upload-profile")
async def upload_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.user = Depends(oauth2.get_current_user)
):
    # Validate file extension
    allowed_extensions = {"jpg", "jpeg", "png", "webp"}
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only jpg, jpeg, png, and webp are allowed."
        )

    # Validate file size (max 5 MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large. Maximum size allowed is 5 MB."
        )

    # Create uploads folder if not exists
    os.makedirs("uploads", exist_ok=True)

    # Delete old file if exists
    if current_user.profile_picture:
        old_path = current_user.profile_picture
        if os.path.exists(old_path) and os.path.isfile(old_path):
            try:
                os.remove(old_path)
            except Exception as e:
                print(f"Error removing old profile picture: {e}")

    # Generate unique filename
    filename = f"profile_{current_user.id}_{int(time.time())}.{file_ext}"
    relative_path = f"uploads/{filename}"

    # Save the file
    try:
        with open(relative_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save profile picture."
        )

    # Update database
    current_user.profile_picture = relative_path
    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile picture updated",
        "profile_picture": relative_path
    }