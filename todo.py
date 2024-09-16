from task import Task
import json

# Global list to store tasks
tasks = []

# add tasks
def add_task(description):
    task = Task(description)
    tasks.append(task)
    save_tasks_to_file()  # Save after adding task
    return f'Task "{description}" added.'


def list_tasks():
    if not tasks:
        return "No tasks available."
    else:
        task_list = ""
        for index, task in enumerate(tasks, start=1):
            status = "[✓]" if task.completed else "[✗]"
            task_list += f"{index}. {task.description} {status}\n"
        return task_list.strip()  # Strip the last newline

#delete
def delete_task(task_number):
    try:
        task = tasks.pop(task_number - 1)
        return f'Task "{task.description}" deleted.'
    except IndexError:
        return "Invalid task number."
    
#Mark Complete
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
        task_data = [{'description': task.description, 'completed': task.completed} for task in tasks]
        json.dump(task_data, file)

def load_tasks_from_file(file_name='tasks.json'):
    try:
        with open(file_name, 'r') as file:
            task_data = json.load(file)
            for task in task_data:
                loaded_task = Task(task['description'])
                loaded_task.completed = task['completed']
                tasks.append(loaded_task)
    except FileNotFoundError:
        # If the file doesn't exist, we start with an empty task list
        pass


# CLI logic moved to a separate function for manual usage
def run_cli():
    while True:
        print("\nCommands: add, list, complete, delete, quit")
        command = input("Enter command: ").strip().lower()

        if command == "add":
            task_desc = input("Enter task description: ").strip()
            print(add_task(task_desc))
        elif command == "list":
            print(list_tasks())
        elif command == "complete":
            task_number = int(input("Enter task number to mark complete: ").strip())
            print(mark_task_complete(task_number))
        elif command == "delete":
            task_number = int(input("Enter task number to delete: ").strip())
            print(delete_task(task_number))
        elif command == "quit":
            break
        else:
            print("Invalid command.")
            
if __name__ == "__main__":
    load_tasks_from_file()
    run_cli()
