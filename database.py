# from mongoengine import connect

# def get_db():
#     try:
#         # Connect to MongoDB
#         connect(
#             db="Final_Authentication",
#             host="mongodb+srv://dppatel:Admin1234@cluster0.ugxqzd8.mongodb.net/Final_Authentication?retryWrites=true&w=majority",
#             alias="default",
#             ssl=True  # Set to True for MongoDB Atlas, as SSL/TLS is required
#         )
#         print("Database connected successfully.")
#     except Exception as e:
#         print(f"Error connecting to database: {e}")
#         raise  # Optionally re-raise the exception after logging it
from mongoengine import connect
import certifi

def get_db():
    try:
        # Connect to MongoDB with certifi for SSL certificates
        connect(
            db="Final_Authentication",
            host="mongodb+srv://dppatel:Admin1234@cluster0.ugxqzd8.mongodb.net/Final_Authentication?retryWrites=true&w=majority",
            alias="default",
            tls=True,  # Use TLS (SSL) for connection
            tlsCAFile=certifi.where()  # Use certifi's CA bundle for SSL certificate verification
        )
        print("Database connected successfully.")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise  # Optionally re-raise the exception after logging it
