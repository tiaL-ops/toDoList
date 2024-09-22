from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from sqlalchemy.orm import sessionmaker
from db.models import Task
from sqlalchemy import create_engine

# Set up Flask app and CORS
app = Flask(__name__)
CORS(app)

# Initialize SocketIO with CORS enabled
socketio = SocketIO(app, cors_allowed_origins="*")

# Set up SQLite database connection and SQLAlchemy session
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()



#load_tasks_from_file()

# Get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    all_tasks = session.query(Task).all()
    task_data = [
        {
            'id': task.id,
            'description': task.description, 
            'completed': task.completed, 
            'priority': task.priority,
            'category': task.category,
            'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None
        } for task in all_tasks
    ]
    return jsonify({'tasks': task_data})



@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    description = data.get('description')
    priority = data.get('priority', 'Medium')
    category = data.get('category', 'General')
    deadline = data.get('deadline', None)

    if deadline:
        deadline = datetime.strptime(deadline, '%Y-%m-%d')

    # Create and add task to the database
    new_task = Task(description=description, priority=priority, category=category, deadline=deadline)
    session.add(new_task)
    session.commit()

    # Emit task update to all clients
    socketio.emit('task_update', {
        'id': new_task.id,
        'description': new_task.description,
        'priority': new_task.priority,
        'category': new_task.category,
        'deadline': new_task.deadline.strftime('%Y-%m-%d') if new_task.deadline else None,
        'completed': new_task.completed
    })

    return jsonify({"message": f"Task '{description}' added.", "status": "success"}), 201




@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_api(task_id):
    # Find the task by ID
    task_to_delete = session.query(Task).filter_by(id=task_id).first()

    if not task_to_delete:
        return jsonify({"message": "Task not found.", "status": "error"}), 404

    # Delete the task
    session.delete(task_to_delete)
    session.commit()

    # Emit the task deletion to all clients
    socketio.emit('task_deleted', {'task_id': task_id})

    return jsonify({"message": f"Task '{task_to_delete.description}' deleted.", "status": "success"})




@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    # Find the task by ID
    task_to_complete = session.query(Task).filter_by(id=task_id).first()

    if not task_to_complete:
        return jsonify({"message": "Task not found.", "status": "error"}), 404

    if task_to_complete.completed:
        return jsonify({"message": "Task already completed.", "status": "error"}), 400

    # Mark the task as complete
    task_to_complete.completed = True
    task_to_complete.completed_on = datetime.now()
    session.commit()

    # Emit the task completion event
    socketio.emit('task_completed', {'task_id': task_id})

    return jsonify({"message": f"Task '{task_to_complete.description}' marked as complete.", "status": "success"})

