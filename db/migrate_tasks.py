import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Task  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from todo import load_tasks_from_file  

engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()


def migrate_tasks_to_database():
    try:
        tasks_from_json = load_tasks_from_file()  # Load tasks from the JSON file
        for task in tasks_from_json:
            # Add each Task object to the session
            session.add(task)

        
        session.commit()
        print(f"Migrated {len(tasks_from_json)} tasks to the database.")
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(f"Error occurred during migration: {e}")
    finally:
        session.close()

# Run the migration
if __name__ == "__main__":
    migrate_tasks_to_database()
