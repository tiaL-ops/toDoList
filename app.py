from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask import send_from_directory 

from db.models import Task, User, db

# Load environment variables
load_dotenv()

# Set up Flask app
app = Flask(__name__, static_folder='build')

# Configure CORS to allow requests from the frontend
CORS(app)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize db with app
db.init_app(app)

migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*")

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
jwt = JWTManager(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()




# Task routes
@app.route('/api/tasks', methods=['GET'])
@csrf.exempt
def get_tasks():
    all_tasks = db.session.query(Task).all()
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
@csrf.exempt
@jwt_required()  
def create_task():
    # Get the current user's ID from the JWT token
    current_user_id = get_jwt_identity()

    # Get task data from the request body
    data = request.get_json()
    description = data.get('description')
    priority = data.get('priority', 'Medium')
    category = data.get('category', 'General')
    deadline = data.get('deadline', None)

    # Handle deadline conversion from string to date object
    if deadline:
        try:
            deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD.", "status": "error"}), 400
    else:
        deadline = None

    # Create a new task for the current user
    new_task = Task(
        description=description,
        priority=priority,
        category=category,
        deadline=deadline,
        user_id=current_user_id  # Assign task to the authenticated user
    )

    try:
        # Add and commit the new task to the database
        db.session.add(new_task)
        db.session.commit()

        # Emit task update to all clients via socket
        socketio.emit('task_update', {
            'id': new_task.id,
            'description': new_task.description,
            'priority': new_task.priority,
            'category': new_task.category,
            'deadline': new_task.deadline.strftime('%Y-%m-%d') if new_task.deadline else None,
            'completed': new_task.completed,
            'user_id': new_task.user_id  
        })

        return jsonify({"message": f"Task '{description}' added.", "status": "success"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding task.", "status": "error", "error": str(e)}), 500


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@csrf.exempt
def delete_task_api(task_id):
    # Find the task by ID
    task_to_delete = db.session.query(Task).filter_by(id=task_id).first()

    if not task_to_delete:
        return jsonify({"message": "Task not found.", "status": "error"}), 404

    # Delete the task
    db.session.delete(task_to_delete)
    db.session.commit()

    # Emit the task deletion to all clients
    socketio.emit('task_deleted', {'task_id': task_id})

    return jsonify({"message": f"Task '{task_to_delete.description}' deleted.", "status": "success"})

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
@csrf.exempt
def complete_task(task_id):
    # Find the task by ID
    task_to_complete = db.session.query(Task).filter_by(id=task_id).first()

    if not task_to_complete:
        return jsonify({"message": "Task not found.", "status": "error"}), 404

    if task_to_complete.completed:
        return jsonify({"message": "Task already completed.", "status": "error"}), 400

    # Mark the task as complete
    task_to_complete.completed = True
    task_to_complete.completed_on = datetime.now()
    db.session.commit()

    # Emit the task completion event
    socketio.emit('task_completed', {'task_id': task_id})

    return jsonify({"message": f"Task '{task_to_complete.description}' marked as complete.", "status": "success"})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@csrf.exempt
def edit_task(task_id):
    # Find the task by ID
    task_to_edit = db.session.query(Task).filter_by(id=task_id).first()

    if not task_to_edit:
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
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD.", "status": "error"}), 400
    else:
        task_to_edit.deadline = None

    try:
        # Commit the changes to the database
        db.session.commit()

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
        db.session.rollback()
        return jsonify({"message": "Error updating task.", "status": "error", "error": str(e)}), 500

from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['POST'])
@csrf.exempt
def register():
    data = request.get_json()

    # Validate the input
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Missing username or password"}), 400

    # Check if the username is already taken
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"message": "Username already taken"}), 400

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
        db.session.rollback()
        return jsonify({"message": "Error registering user", "error": str(e)}), 500

@app.route('/login', methods=['POST'])
@csrf.exempt
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()

    # Check if the user exists and password is correct
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@app.route('/api/users', methods=['GET'])
@csrf.exempt
def get_users():
    try:
        # Query all users from the database
        users = db.session.query(User).all()
        users_data = [
            {
                'id': user.id,
                'username': user.username,
            } for user in users
        ]
        return jsonify({"users": users_data}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Error fetching users.", "status": "error", "error": str(e)}), 500

@app.route('/refresh', methods=['POST'])
@csrf.exempt
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
