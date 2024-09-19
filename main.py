import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from todo import add_task, delete_task, mark_task_complete, save_tasks_to_file, load_tasks_from_file, tasks  # Import from todo.py


def update_task_list():
    task_listbox.delete(0, tk.END)  # Clear current task list
    for index, task in enumerate(tasks, start=1):
        status = "[✓]" if task.completed else "[✗]"
        deadline_str = task.deadline.strftime('%Y-%m-%d') if task.deadline else "No deadline"
        task_listbox.insert(tk.END, f"{index}. {task.description} {status} (Priority: {task.priority}) Deadline: {deadline_str}")


# Handle deleting a task
def handle_delete_task():
    try:
        selected_task_index = task_listbox.curselection()[0]  # Get selected task index
        delete_task(selected_task_index + 1)  # Adjust index for 1-based list in todo.py
        update_task_list()  # Refresh the task list
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Handle marking a task as complete
def handle_complete_task():
    try:
        selected_task_index = task_listbox.curselection()[0]  # Get selected task index
        mark_task_complete(selected_task_index + 1)  # Adjust for 1-based index
        update_task_list()  # Refresh the task list
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")

# Handle adding a new task
def handle_add_task():
    description = task_entry.get()
    priority = priority_var.get()  # Get priority from dropdown
    category = category_var.get()  # Get category from dropdown
    deadline_input = deadline_entry.get()  # Get deadline from entry field

    # Validate description
    if not description:
        messagebox.showwarning("Input Error", "Please enter a task description.")
        return
    
    # Validate deadline
    if deadline_input:
        try:
            deadline = datetime.strptime(deadline_input, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid deadline format. Use YYYY-MM-DD.")
            return
    else:
        deadline = None
    
    # Add task using the function from todo.py
    add_task(description, priority=priority, category=category, deadline=deadline)
    
    # Clear input fields
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    
    # Update the task list in the GUI
    update_task_list()

# Create the main Tkinter window
root = tk.Tk()
root.title("Task Manager")
root.geometry("500x500")

# Entry field for task description
tk.Label(root, text="Task Description").pack(pady=5)
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)

# Dropdown for task priority
tk.Label(root, text="Task Priority").pack(pady=5)
priority_var = tk.StringVar(value="Medium")
priority_dropdown = tk.OptionMenu(root, priority_var, "Low", "Medium", "High")
priority_dropdown.pack(pady=5)

# Dropdown for task category
tk.Label(root, text="Task Category").pack(pady=5)
category_var = tk.StringVar(value="General")
category_dropdown = tk.OptionMenu(root, category_var, "General", "Work", "Personal", "Other")
category_dropdown.pack(pady=5)

# Entry field for task deadline
tk.Label(root, text="Task Deadline (YYYY-MM-DD)").pack(pady=5)
deadline_entry = tk.Entry(root, width=20)
deadline_entry.pack(pady=5)

# Button to add a new task
add_task_button = tk.Button(root, text="Add Task", command=handle_add_task)
add_task_button.pack(pady=10)

# Listbox to display tasks
task_listbox = tk.Listbox(root, width=50, height=10)
task_listbox.pack(pady=10)

# Buttons for marking complete and deleting tasks
complete_button = tk.Button(root, text="Mark Complete", command=handle_complete_task)
complete_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=handle_delete_task)
delete_button.pack(pady=5)

# Load tasks from file when the GUI starts
load_tasks_from_file()
update_task_list()


# Save tasks to file when the window is closed
def on_closing():
    save_tasks_to_file()
    root.destroy()

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the Tkinter event loop
root.mainloop()
