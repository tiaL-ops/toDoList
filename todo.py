from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Task
from datetime import datetime
import json 
import uuid
# Set up SQLite database connection
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()

tasks=[]
# Add a new task to the database
def add_task(description, priority="Medium", category="General", deadline=None):
    new_task = Task(description=description, priority=priority, deadline=deadline, completed=False)
    session.add(new_task)
    session.commit()
    return f'Task "{description}" added with priority {priority} and deadline {deadline if deadline else "None"}.'

# List all tasks from the database
def list_tasks():
    all_tasks = session.query(Task).all()

    if not all_tasks:
        return "No tasks available."

    today = datetime.datetime.now()
    task_list = ""
    task_counter = 1

    tasks_by_category = {}
    for task in all_tasks:
        if task.category not in tasks_by_category:
            tasks_by_category[task.category] = []
        tasks_by_category[task.category].append(task)

    for category, tasks_in_category in tasks_by_category.items():
        task_list += f"\nCategory: {category}\n"
        for task in tasks_in_category:
            status = "[✓]" if task.completed else "[✗]"
            deadline_str = task.deadline.strftime('%Y-%m-%d') if task.deadline else "No deadline"
            overdue_warning = ""

            if task.deadline and task.deadline < today and not task.completed:
                overdue_warning = " (OVERDUE!)"

            task_list += f"  {task_counter}. {task.description} {status} (Priority: {task.priority}) Deadline: {deadline_str}{overdue_warning}\n"
            task_counter += 1

    return task_list.strip()

# Delete a task by its ID
def delete_task(task_id):
    task_to_delete = session.query(Task).filter_by(id=task_id).first()

    if task_to_delete:
        session.delete(task_to_delete)
        session.commit()
        return f'Task "{task_to_delete.description}" deleted.'
    else:
        return "Task not found."

# Mark a task as complete
def mark_task_complete(task_id):
    task = session.query(Task).filter_by(id=task_id).first()
    
    if task:
        if task.completed:
            return f'Task "{task.description}" is already completed.'
        
        task.completed = True
        task.completed_on = datetime.datetime.now()
        session.commit()
        
        return f'Task "{task.description}" marked as complete.'
    else:
        return "Task not found."

def load_tasks_from_file(file_name='tasks.json'):
    tasks = []  # Initialize the list to store tasks
    try:
        with open(file_name, 'r') as file:
            task_data = json.load(file)

            for task in task_data:
                # Convert deadline string to datetime object if applicable
                deadline_str = task.get('deadline')
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d') if deadline_str else None

                # Create a new Task object without assigning 'id' (SQLite will auto-increment it)
                loaded_task = Task(
                    description=task['description'],
                    priority=task.get('priority', 'Medium'),
                    category=task.get('category', 'General'),
                    deadline=deadline,
                    completed=task.get('completed', False)
                )

                # Append the task to the list
                tasks.append(loaded_task)

    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []

    return tasks  # Return the list of tasks