from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class SignUp(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    role: Optional[str] = None
    password: str
    status: bool = False
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data):
        super().__init__(**data)
        now = datetime.utcnow()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now

class Login(BaseModel):
    email: EmailStr
    password: str
