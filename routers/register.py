from fastapi import APIRouter, HTTPException
from models.user import User
from crud.user import create_user, get_user_by_username

router = APIRouter()

@router.post("/register")
async def register_user(user: User):
    try:
        existing_user = get_user_by_username(user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
    except HTTPException as e:
        if e.status_code == 404:  # User not found, safe to register
            create_user(user)
            return {"message": "User registered successfully", "username": user.username}
        else:
            raise HTTPException(status_code=e.status_code, detail=e.detail)