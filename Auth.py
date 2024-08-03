from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()  # Ensure this line is present

class AuthHandler:
    security = OAuth2PasswordBearer(tokenUrl="token")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.getenv("SECRET_KEY")

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, email: str) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
            "sub": email
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: str = Depends(security)):
        return self.decode_token(auth)
