from task import Task

# Global list to store tasks
tasks = []

# Function to add tasks
def add_task(description):
    task = Task(description)
    tasks.append(task)
    return f'Task "{description}" added.'

# Function to list all tasks
def list_tasks():
    if not tasks:
        return "No tasks available."
    else:
        task_list = ""
        for index, task in enumerate(tasks, start=1):
            task_list += f"{index}. {task}\n"
        return task_list.strip()

# CLI logic moved to a separate function for manual usage
def run_cli():
    while True:
        print("\nCommands: add, list, quit")
        command = input("Enter command: ").strip().lower()

        if command == "add":
            task_desc = input("Enter task description: ").strip()
            print(add_task(task_desc))
        elif command == "list":
            print(list_tasks())
        elif command == "quit":
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    run_cli()
