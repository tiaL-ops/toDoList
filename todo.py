from task import Task

# Global list to store tasks
tasks = []

# add tasks
def add_task(description):
    task = Task(description)
    tasks.append(task)
    return f'Task "{description}" added.'

# List all tasks
def list_tasks():
    if not tasks:
        return "No tasks available."
    else:
        task_list = ""
        for index, task in enumerate(tasks, start=1):
            task_list += f"{index}. {task}\n"
        return task_list.strip()

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
    run_cli()
