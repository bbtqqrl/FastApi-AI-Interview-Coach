import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")
PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH")
ALGORITHM = os.getenv("ALGORITHM", "RS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "r") as f:
    PUBLIC_KEY = f.read()

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, 
        PRIVATE_KEY, 
        algorithm=ALGORITHM
        )
    return encoded_jwt

def verify_token(token: str) -> dict:
    payload = jwt.decode(
        token, 
        PUBLIC_KEY, 
        algorithms=[ALGORITHM]
        )
    return payload

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode() 

def validate_password(
        password: str, 
        hashed_password: str
        ) -> bool:
    
    return bcrypt.checkpw(password.encode(), hashed_password.encode())