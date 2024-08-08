from mongoengine import *
class SignUp(Document):
    firstname=StringField(required=True)
    lastname=StringField(required=True)
    email=EmailField(required=True,unique=True)
    role=StringField()
    password=StringField()
    status=BooleanField(required=True)
    created_at=DateTimeField(required=True,auto_now_add=True)
    updated_at=DateTimeField(required=True,auto_now=True)

class Login(Document):
    email=EmailField(required=True)
    password=StringField(required=True)