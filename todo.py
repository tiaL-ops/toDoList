from task import Task
from datetime import datetime
import json

# Global list to store tasks
tasks = []

# add tasks
def add_task(description, priority="Medium", category="General", deadline=None):
    task = Task(description, priority=priority, deadline=deadline, category=category)
    tasks.append(task)
    save_tasks_to_file()  
    return f'Task "{description}" added with priority {priority} and deadline {deadline if deadline else "None"}.'

def list_tasks():
    if not tasks:
        return "No tasks available."
    else:
        today = datetime.now()
        task_list = ""
        task_counter = 1  

        tasks_by_category = {}
        for task in tasks:
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
                task_counter += 1  # Increment the counter after each task

        return task_list.strip()

# delete
def delete_task(task_number):
    try:
        task = tasks.pop(task_number - 1)
        return f'Task "{task.description}" deleted.'
    except IndexError:
        return "Invalid task number."

# Mark Complete
def mark_task_complete(task_number):
    try:
        task = tasks[task_number - 1]
        if task.completed:
            return f'Task "{task.description}" is already completed.'
        task.mark_complete()
        return f'Task "{task.description}" marked as complete.'
    except IndexError:
        return "Invalid task number."

def save_tasks_to_file(file_name='tasks.json'):
    with open(file_name, 'w') as file:
        task_data = [
            {
                'description': task.description, 
                'completed': task.completed, 
                'priority': task.priority,
                'category': task.category,
                'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None
            } for task in tasks
        ]
        json.dump(task_data, file)

def load_tasks_from_file(file_name='tasks.json'):
    try:
        with open(file_name, 'r') as file:
            task_data = json.load(file)
            for task in task_data:
                deadline_str = task.get('deadline')
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d') if deadline_str else None
                category = task.get('category', 'General')
                loaded_task = Task(
                    task['description'],
                    priority=task.get('priority', 'Medium'),
                    category=category,
                    deadline=deadline
                )
                loaded_task.completed = task.get('completed', False)
                tasks.append(loaded_task)
    except FileNotFoundError:
        pass
