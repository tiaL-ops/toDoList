from app import app  
from db.models import Task, User 

# Use the Flask app context to perform queries
with app.app_context():
    tasks = Task.query.all()
    users = User.query.all()

    print(f"Found {len(tasks)} tasks in the database.")
    print(f"Found {len(users)} users in the database.")
