from app import User, db
from werkzeug.security import generate_password_hash


new_user = User(username="testuser", password_hash=generate_password_hash("testpassword"))


db.session.add(new_user)
db.session.commit()
