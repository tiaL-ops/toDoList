from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

def init_jwt(app):
    # Retrieve the JWT secret key from the environment variable
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Initialize JWT manager with the app
    jwt = JWTManager(app)
    return jwt
