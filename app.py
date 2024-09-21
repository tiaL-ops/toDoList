from flask import Flask, request, jsonify
from datetime import datetime
from todo import tasks, add_task, delete_task, mark_task_complete, load_tasks_from_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)  # Cross-Origin Resource Sharing (CORS)
socketio = SocketIO(app, cors_allowed_origins="*")  # Initialize SocketIO with CORS enabled

# Load tasks from the file when the app starts
load_tasks_from_file()

# Get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    task_data = [
        {
            'id': task.id,
            'description': task.description, 
            'completed': task.completed, 
            'priority': task.priority,
            'category': task.category,
            'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None
        } for task in tasks
    ]
    return jsonify({'tasks': task_data})


# Add a task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    description = data.get('description')
    priority = data.get('priority', 'Medium')
    category = data.get('category', 'General')
    deadline = data.get('deadline', None)

    if deadline:
        deadline = datetime.strptime(deadline, '%Y-%m-%d')

    result = add_task(description, priority, category, deadline)

   
    new_task = {
        'description': description,
        'priority': priority,
        'category': category,
        'deadline': deadline.strftime('%Y-%m-%d') if deadline else None,
        'completed': False
    }
    socketio.emit('task_update', new_task)  # Emit 'task_update' event
    
    return jsonify({"message": result, "status": "success"}), 201



# Delete a task
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task_api(task_id):
    result = delete_task(task_id)  # Use task_id to delete the task
    if result.startswith("Task not found"):
        return jsonify({"message": result, "status": "error"}), 404
    return jsonify({"message": result, "status": "success"})



# Mark a task as complete
@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    result = mark_task_complete(task_id)

   
    socketio.emit('task_completed', {'task_id': task_id})

    return jsonify(result)

if __name__ == "__main__":
    socketio.run(app, debug=True)
