from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import user as user_schema
from ..services.auth_service import register_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=user_schema.UserResponse)
def register(user: user_schema.UserCreate):
    return register_user(user)

@router.post("/login")
def login(user: user_schema.UserLogin):
    return login_user(user)