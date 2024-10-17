from models import Task,User

from werkzeug.security import generate_password_hash

tasks = Task.query.all()
users = User.query.all()

print(f"Found {len(tasks)} tasks in the database.")
print(f"Found {len(users)} users in the database.")
