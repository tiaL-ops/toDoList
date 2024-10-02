from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from db.models import Task
from db.user_models import User
from collections import deque
from sqlalchemy.exc import SQLAlchemyError

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
# Load environment variables early
load_dotenv()

# Set up Flask app and CORS
app = Flask(__name__)
CORS(app)

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
jwt = JWTManager(app)

# Initialize SocketIO with CORS enabled
socketio = SocketIO(app, cors_allowed_origins="*")

# Set up SQLite database connection and SQLAlchemy session
engine = create_engine('sqlite:///tasks.db')
Session = scoped_session(sessionmaker(bind=engine))

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

# Task routes
@app.route('/api/tasks', methods=['GET'])
#@jwt_required()
def get_tasks():
    session = Session()
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
    session.close()
    return jsonify({'tasks': task_data})

@app.route('/api/tasks', methods=['POST'])
#@jwt_required()
def create_task():
    session = Session()
    data = request.get_json()
    description = data.get('description')
    priority = data.get('priority', 'Medium')
    category = data.get('category', 'General')
    deadline = data.get('deadline', None)

    # Handle the deadline conversion
    if deadline:
        try:
            deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD.", "status": "error"}), 400
    else:
        deadline = None

    # Create and add the task to the database
    new_task = Task(description=description, priority=priority, category=category, deadline=deadline)

    try:
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
    except Exception as e:
        session.rollback()
        return jsonify({"message": "Error adding task.", "status": "error", "error": str(e)}), 500
    finally:
        session.close()

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
#@jwt_required()
def delete_task_api(task_id):
    session = Session()
    # Find the task by ID
    task_to_delete = session.query(Task).filter_by(id=task_id).first()

    if not task_to_delete:
        session.close()
        return jsonify({"message": "Task not found.", "status": "error"}), 404

    # Delete the task
    session.delete(task_to_delete)
    session.commit()

    # Emit the task deletion to all clients
    socketio.emit('task_deleted', {'task_id': task_id})

    session.close()
    return jsonify({"message": f"Task '{task_to_delete.description}' deleted.", "status": "success"})

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
#@jwt_required()
def complete_task(task_id):
    session = Session()
    # Find the task by ID
    task_to_complete = session.query(Task).filter_by(id=task_id).first()

    if not task_to_complete:
        session.close()
        return jsonify({"message": "Task not found.", "status": "error"}), 404

    if task_to_complete.completed:
        session.close()
        return jsonify({"message": "Task already completed.", "status": "error"}), 400

    # Mark the task as complete
    task_to_complete.completed = True
    task_to_complete.completed_on = datetime.now()
    session.commit()

    # Emit the task completion event
    socketio.emit('task_completed', {'task_id': task_id})

    session.close()
    return jsonify({"message": f"Task '{task_to_complete.description}' marked as complete.", "status": "success"})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
#@jwt_required()
def edit_task(task_id):
    session = Session()
    # Find the task by ID
    task_to_edit = session.query(Task).filter_by(id=task_id).first()

    if not task_to_edit:
        session.close()
        return jsonify({"message": "Task not found.", "status": "error"}), 404

    # Get the updated data from the request
    data = request.get_json()

    # Update the task fields
    task_to_edit.description = data.get('description', task_to_edit.description)
    task_to_edit.priority = data.get('priority', task_to_edit.priority)
    task_to_edit.category = data.get('category', task_to_edit.category)

    deadline = data.get('deadline', None)
    if deadline:
        try:
            task_to_edit.deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        except ValueError:
            session.close()
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD.", "status": "error"}), 400
    else:
        task_to_edit.deadline = None

    try:
        # Commit the changes to the database
        session.commit()

        # Emit the updated task to all clients
        socketio.emit('task_update', {
            'id': task_to_edit.id,
            'description': task_to_edit.description,
            'priority': task_to_edit.priority,
            'category': task_to_edit.category,
            'deadline': task_to_edit.deadline.strftime('%Y-%m-%d') if task_to_edit.deadline else None,
            'completed': task_to_edit.completed
        })

        return jsonify({"message": f"Task '{task_to_edit.description}' updated.", "status": "success"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"message": "Error updating task.", "status": "error", "error": str(e)}), 500
    finally:
        session.close()

# User authentication and JWT routes
@app.route('/login', methods=['POST'])
def login():
    session = Session()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = session.query(User).filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        session.close()
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        session.close()
        return jsonify({"message": "Invalid credentials"}), 401



@app.route('/register', methods=['POST'])
@csrf.exempt 
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Missing username or password"}), 400
    # Simulate successful registration
    return jsonify({"message": "User registered successfully"}), 201






@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200


@app.route('/test', methods=['GET'])

def test():
    return jsonify({"message": "Test successful!"}), 200


if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False)

