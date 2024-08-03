from Schemas import SignUp,Login
from Auth import AuthHandler
from pymongo.database import Database
from database import get_db
from bson import ObjectId
Auth=AuthHandler()
def signup(db:Database,user:SignUp):
    hashed_password=Auth.get_password_hash(user.password)
    signup_db={
        "firstname":user.firstname,
        "lastname":user.lastname,
        "email":user.email,
        "role":user.role,
        "password":hashed_password,
        "status":user.status,
        "created_at":user.created_at,
        "updated_at":user.updated_at
    }
    result=db["SignUp"].insert_one(signup_db)
    return {
        "firstname":user.firstname,
        "lastname":user.lastname,
        "email":user.email,
        "role":user.role,
        "created_at":user.created_at,
        "updated_at":user.updated_at,
        "ID":result.inserted_id
    }

def login(db:Database,user:Login):
    login_db=db["SignUp"].find_one({"email":user.email})
    if not login_db:
        return None
    if not Auth.verify_password(user.password,login_db["password"]):
        return None
    return login_db