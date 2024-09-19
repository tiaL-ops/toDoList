from flask import Flask, jsonify, request
from flask_cors import CORS
from todo import add_task, delete_task, mark_task_complete, tasks, save_tasks_to_file, load_tasks_from_file

app = Flask(__name__)
CORS(app)


load_tasks_from_file()

@app.route('/')
def home():
    return "<h1>Welcome to the To-Do API</h1><p>Use <code>/tasks</code> to view tasks.</p>"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Return tasks as JSON
    task_list = [
        {
            'id': index + 1,
            'description': task.description,
            'priority': task.priority,
            'category': task.category,
            'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None,
            'completed': task.completed
        }
        for index, task in enumerate(tasks)
    ]
    return jsonify(task_list), 200


@app.route('/tasks', methods=['POST'])
def api_add_task():
    data = request.json
    description = data.get('description')
    priority = data.get('priority', 'Medium')
    category = data.get('category', 'General')
    deadline = data.get('deadline')

  
    new_task = Task(description, priority=priority, category=category, deadline=deadline)
    tasks.append(new_task)
    save_tasks_to_file()

    return jsonify({'message': f'Task "{description}" added successfully.'}), 201

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def api_mark_task_complete(task_id):
    try:
        
        result = mark_task_complete(task_id)
        save_tasks_to_file()
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    try:
        result = delete_task(task_id)
        save_tasks_to_file()
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
