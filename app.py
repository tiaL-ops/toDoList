from flask import Flask, request, jsonify, make_response
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
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect
from collections import deque
from flask import send_from_directory 

# Load environment variables
load_dotenv()

# Set up Flask app
app = Flask(__name__, static_folder='build')


# Configure CORS to allow requests from the frontend
CORS(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy, SocketIO, and Migrate
db = SQLAlchemy(app)  # Using SQLAlchemy as Flask's ORM
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*")

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
jwt = JWTManager(app)

# Set up direct SQLAlchemy engine and scoped session if needed
engine = create_engine('sqlite:///tasks.db')
Session = scoped_session(sessionmaker(bind=engine))

# Import your models (User and Task) after initializing db and app
from db.user_models import User
from db.models import Task

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

@app.route('/login', methods=['POST'])
def login():
    session = Session()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        # Check if the user exists
        user = session.query(User).filter_by(username=username).first()

        if not user:
            # Return a specific message if the user does not exist
            session.close()
            return jsonify({"message": "User does not exist", "status": "error"}), 404

        # Check if the password matches
        if not user.check_password(password):
            session.close()
            return jsonify({"message": "Incorrect password", "status": "error"}), 401

        # Generate access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        session.close()

        # Return tokens on successful login
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    except Exception as e:
        session.close()
        # General error handler for any other issues
        return jsonify({"message": "An error occurred during login", "status": "error", "error": str(e)}), 500



@app.route('/register', methods=['POST'])
@csrf.exempt
def register():
    data = request.get_json()

    # Validate the input
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Missing username or password"}), 400

    # Hash the password for security
    hashed_password = generate_password_hash(data['password'])

    # Create a new user object
    new_user = User(username=data['username'], password_hash=hashed_password)

    try:
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({"message": "Error registering user", "error": str(e)}), 500


@app.route('/api/users', methods=['GET'])
# @jwt_required()  
def get_users():
    session = Session()
    try:
        # Query all users from the database
        users = session.query(User).all()
        users_data = [
            {
                'id': user.id,
                'username': user.username,
            } for user in users
        ]
        session.close()
        return jsonify({"users": users_data}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"message": "Error fetching users.", "status": "error", "error": str(e)}), 500
    finally:
        session.close()


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200


@app.route('/test', methods=['GET', 'POST'])
def test():
    response = make_response(jsonify({"message": "Hello, CORS manually enabled!"}))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    socketio.run(app, debug=True, use_reloader=False)

