from flask_jwt_extended import JWTManager

def init_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Ensure you change this to a secure secret
    jwt = JWTManager(app)
    return jwt
