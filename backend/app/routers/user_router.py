from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.crud.user_crud import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
    update_user,
    delete_user
)
from app.database import db_dependency as db
from app.auth import user_dependency as user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: db):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    existing_username = get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    try:
        new_user = create_user(db, user)
        return new_user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user due to integrity error"
        )


@router.get("/get_user/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_user(user: user, db: db, user_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put("/update/{user_id}", response_model=UserResponse)
def update_user_details(user: user, db: db, user_id: int, user_update: UserUpdate):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    updated_user = update_user(db, user_id, username=user_update.username, email=user_update.email,
                               is_active=user_update.is_active)
    return updated_user


@router.delete("/delete/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def delete_user_account(user: user, db: db, user_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    deleted_user = delete_user(db, user_id)
    return deleted_user
