from models.user import User
from database.connection import db
import bcrypt
from fastapi import HTTPException
import jwt
import datetime

SECRET_KEY = "your_secret_key"

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(user: User):
    hashed_password = hash_password(user.password)
    user_data = {
        "username": user.username,
        "password": hashed_password
    }
    db.users.insert_one(user_data)
    print(f"User {user.username} saved to the database")

def get_user_by_username(username: str):
    user_data = db.users.find_one({"username": username})
    if user_data:
        return User(**user_data)
    else:
        raise HTTPException(status_code=404, detail="User not found")

def create_access_token(username: str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({"sub": username, "exp": expiration}, SECRET_KEY, algorithm="HS256")
    return token

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")