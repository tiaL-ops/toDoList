import sys
import os
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Task  #
from todo import load_tasks_from_file

# Set up the database connection
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()

# Function to migrate tasks to the SQL database

def migrate_tasks_to_database():
    tasks_from_json = load_tasks_from_file()  # Assuming this loads your tasks from tasks.json

    for task_data in tasks_from_json:
        # Convert deadline string to datetime object, if applicable
        deadline_str = task_data.get('deadline')
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d') if deadline_str else None

        # Create a new SQLAlchemy Task object
        new_task = Task(
            id=task_data['id'],
            description=task_data['description'],
            priority=task_data.get('priority', 'Medium'),
            category=task_data.get('category', 'General'),
            deadline=deadline,  # This is now a datetime object
            completed=task_data.get('completed', False)
        )
        session.add(new_task)

    session.commit()
    print(f"Migrated {len(tasks_from_json)} tasks to the database.")

# Run the migration
if __name__ == "__main__":
    migrate_tasks_to_database()
