from pymongo import MongoClient
client=MongoClient("mongodb+srv://dppatel:Admin1234@cluster0.ugxqzd8.mongodb.net/")
try:
    client.admin.command("ping")
    print("Connected Successfully")
except Exception as e:
    print(e)
db=client.get_database("Authentication")
def get_db():
    return db