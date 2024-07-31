import logging
from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import user as user_schema
from ..services.auth_service import register_user, login_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=user_schema.UserResponse)
def register(user: user_schema.UserCreate):
    logger.info(f"Received registration request with username: {user.username}")
    try:
        result = register_user(user)
        logger.info("User registered successfully")
        return result
    except HTTPException as e:
        logger.error(f"Registration failed: {e.detail}")
        raise e

@router.post("/login")
def login(user: user_schema.UserLogin):
    logger.info(f"Received login request with username: {user.username}")
    try:
        result = login_user(user)
        logger.info("Login successful")
        return result
    except HTTPException as e:
        logger.error(f"Login failed: {e.detail}")
        raise e