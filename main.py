from fastapi import FastAPI, Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pymongo.database import Database
from database import get_db
from Models import signup,login
from Schemas import SignUp,Login
from Auth import AuthHandler
from emails_utils import send_verification_email
app=FastAPI()
Auth=AuthHandler()
@app.post("/signup")
async def register(user:SignUp,db:Database=Depends(get_db)):
    signup_db2=db["SignUp"].find_one({"email":user.email})
    if signup_db2:
        raise HTTPException(status_code=401,detail="Username or email already exists")
    signup_result = signup(db, user)

    # Send verification email
    token = Auth.encode_token(user.email)
    send_verification_email(user.email, token)

    return {"message": "User registered successfully. Please check your email to verify your account."}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.post("/token",tags=["authentication"])
async def Access_Login(form_data:OAuth2PasswordRequestForm=Depends(),db:Database=Depends(get_db)):
    userlogin=Login(email=form_data.username,password=form_data.password)
    authenticated_user = login(db, userlogin)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not authenticated_user.get("status"):
        raise HTTPException(status_code=401, detail="Email not verified")
    role=authenticated_user["role"]
    token = Auth.encode_token(authenticated_user["email"])
    return {"access_token": token, "token_type": "bearer","role":role}

@app.get("/verify/{token}")
async def verify_email(token: str, db: Database = Depends(get_db)):
    email = Auth.decode_token(token)
    user = db["SignUp"].find_one({"email": email})
    if user:
        db["SignUp"].update_one({"email": email}, {"$set": {"status": True}})
        return {"message": "Email verified successfully."}
    raise HTTPException(status_code=400, detail="Invalid token or email not found")