from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import get_db  # Assumes this now uses MongoEngine
from Models import signup, login  # Functions now work with MongoEngine
from Schemas import SignUp as MongoSignUp, Login as MongoLogin  # Import MongoEngine schemas
from Pydantic_Schemas import SignUp as PydanticSignUp, Login as PydanticLogin
from Auth import AuthHandler
from emails_utils import send_verification_email
from mongoengine import DoesNotExist

app = FastAPI()
Auth = AuthHandler()

@app.post("/signup")
async def register(user: PydanticSignUp, db=Depends(get_db)):
    # Check if the email already exists
    if MongoSignUp.objects(email=user.email).first():
        raise HTTPException(status_code=401, detail="Username or email already exists")
    
    # Call the signup function
    signup_result = signup(user)

    # Send verification email
    token = Auth.encode_token(user.email)
    send_verification_email(user.email, token)

    return {"message": "User registered successfully. Please check your email to verify your account."}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", tags=["authentication"])
async def access_login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    userlogin = PydanticLogin(email=form_data.username, password=form_data.password)
    authenticated_user = login(userlogin)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not authenticated_user.get("status"):
        raise HTTPException(status_code=401, detail="Email not verified")

    role = authenticated_user["role"]
    token = Auth.encode_token(authenticated_user["email"])

    return {"access_token": token, "token_type": "bearer", "role": role}


@app.get("/verify/{token}")
async def verify_email(token: str, db=Depends(get_db)):
    email = Auth.decode_token(token)
    try:
        user = MongoSignUp.objects.get(email=email)  # Query using MongoEngine
        user.update(set__status=True)  # Update the status field
        return {"message": "Email verified successfully."}
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Invalid token or email not found")
