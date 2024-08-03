from pydantic import BaseModel, EmailStr
from datetime import datetime
class SignUp(BaseModel):
    firstname:str
    lastname:str
    email:EmailStr
    role:str
    password:str
    status:bool=False
    created_at:datetime=datetime.utcnow()
    updated_at:datetime=datetime.utcnow()

class Login(BaseModel):
    email:EmailStr
    password:str
