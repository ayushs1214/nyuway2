from fastapi import HTTPException, status
from pymongo import MongoClient
from passlib.context import CryptContext
from ..config import settings
from ..schemas import user as user_schema
from ..models import user as user_model
from bson import ObjectId
import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = MongoClient(settings.MONGODB_URL)
db = client['nyuway']
users_collection = db['users']

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def register_user(user: user_schema.UserCreate):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = get_password_hash(user.password)
    user_obj = user_model.User(username=user.username, hashed_password=hashed_password)
    result = users_collection.insert_one(user_obj.dict(by_alias=True))
    return user_model.User(**user_obj.dict(by_alias=True))

def login_user(user: user_schema.UserLogin):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": db_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}