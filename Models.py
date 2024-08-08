from Pydantic_Schemas import SignUp as PydanticSignUp, Login as PydanticLogin
from Schemas import SignUp as MongoSignUp, Login as MongoLogin
from Auth import AuthHandler

# Initialize AuthHandler
Auth = AuthHandler()

def signup(user: PydanticSignUp):
    # Convert Pydantic model to MongoEngine model
    mongo_user = MongoSignUp(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        role=user.role,
        password=Auth.get_password_hash(user.password),
        status=False,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    mongo_user.save()  # Save the document to the database

    return {
        "firstname": mongo_user.firstname,
        "lastname": mongo_user.lastname,
        "email": mongo_user.email,
        "role": mongo_user.role,
        "created_at": mongo_user.created_at,
        "updated_at": mongo_user.updated_at,
        "ID": str(mongo_user.id)  # Convert ObjectId to string
    }

def login(user: PydanticLogin):
    # Find a user by email
    login_user = MongoSignUp.objects(email=user.email).first()
    
    if not login_user:
        print(f"No user found with email {user.email}")
        return None

    # Verify the password
    if not Auth.verify_password(user.password, login_user.password):
        print(f"Password verification failed for email {user.email}")
        return None

    return {
        "firstname": login_user.firstname,
        "lastname": login_user.lastname,
        "email": login_user.email,
        "role": login_user.role,
        "status": login_user.status,
        "created_at": login_user.created_at,
        "updated_at": login_user.updated_at,
        "ID": str(login_user.id)  # Convert ObjectId to string
    }
