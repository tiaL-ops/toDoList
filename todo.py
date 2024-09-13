from task import Task
tasks = []

def add_task(description):
    task = Task(description)
    tasks.append(task)
    print(f'Task "{description}" added.')

def list_tasks():
    if not tasks:
        print("No tasks available.")
    else:
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task}")

while True:
    print("\nCommands: add, list, quit")
    command = input("Enter command: ").strip().lower()

    if command == "add":
        task_desc = input("Enter task description: ").strip()
        add_task(task_desc)
    elif command == "list":
        list_tasks()
    elif command == "quit":
        break
    else:
        print("Invalid command.")
