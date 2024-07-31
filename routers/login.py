from fastapi import APIRouter, HTTPException
from models.user import User
from crud.user import get_user_by_username, verify_password, create_access_token

router = APIRouter()

@router.post("/login")
async def login_user(user: User):
    try:
        db_user = get_user_by_username(user.username)
        if verify_password(user.password, db_user.password):
            token = create_access_token(user.username)
            return {"message": "Login successful", "username": user.username, "token": token}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)