
# ToDo List Application

This is a simple ToDo List application that allows users to add, view, and manage tasks. The frontend is built with React, and the backend is built using Flask, which handles task creation, deletion, and completion.

## Features

- Add new tasks with descriptions, priorities, categories, and deadlines.
- View a list of tasks with task details.
- Delete tasks or mark them as completed.
- Persistent storage using a JSON file (or could be a database in the future).
- API built with Flask to handle task management.

---

## Project Timelines (Ongoing ☺️)

| **Day** | **Objective**                               | **Completed**                                  | **Technical Details / Notes**                                                                              |
|---------|---------------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| **1**   | Set Up and Basic Task Addition, Git Initiation | ✅ Initialized project, added task creation     | - Initialized the project with Git for version control.                                                    |
|         |                                              |                                                | - Implemented basic task creation using the `Task` class.                                                  |
|         |                                              |                                                | - Used properties like `description` and `completed` to manage tasks.                                      |
| **2**   | View, Mark Complete, and Delete Tasks       | ✅ Added view, mark complete, and delete features | - Developed `mark_task_complete()` and `delete_task()` functions.                                           |
|         |                                              |                                                | - Implemented task viewing, marking tasks as complete, and deleting tasks from the global task list.        |
|         |                                              |                                                | - Debugged unit tests for task completion and deletion.                                                     |
| **3**   | Save and Load Tasks (File Persistence)      | ✅ Implemented file persistence with JSON       | - Created `save_tasks_to_file()` and `load_tasks_from_file()` for task persistence in a JSON file.          |
|         |                                              |                                                | - Fixed task listing functionality to load tasks from the JSON file.                                       |
| **4**   | Task Priorities                             | ✅ Added task priority feature                  | - Introduced task prioritization (Low, Medium, High) and updated the `Task` class.                         |
|         |                                              |                                                | - Task list can now be sorted by priority and priorities are considered during task addition.               |
| **5**   | Task Deadlines and Alerts                   | ✅ Added deadlines and sorted by timestamp      | - Added `deadline` field to the `Task` class to track due dates.                                           |
|         |                                              |                                                | - Tasks are now sorted by deadline, and overdue tasks can be highlighted.                                   |
| **6**   | Frontend with React                         | ✅ Integrated React for frontend                | - Rebuilt the frontend using React for better UI and state management.                                      |
|         |                                              |                                                | - Created `ToDoForm` for task addition and `ToDoList` to display and manage tasks.                          |
| **7**   | WebSocket for Real-time Updates             | ✅ Added WebSocket support for real-time updates| - Integrated WebSocket (Socket.io) to enable real-time task creation and deletion.                          |
|         |                                              |                                                | - Frontend now updates tasks in real time without page refresh.                                             |
| **8**   | Refactor to SQL                             | ✅ Completed refactor to SQL                    | - Replaced JSON-based task storage with an SQLite database for persistence.                                 |
|         |                                              |                                                | - Refactored backend code to use SQLAlchemy ORM for database operations.                                    |
|         |                                              |                                                | - Implemented data migration from JSON tasks to the SQLite database.                                        |
|         |                                              |                                                | - Ensured task IDs are auto-generated by SQLite and deadlines are handled correctly.                        |
|         |                                              |                                                | - Fixed issues with date formatting and integrated the new database layer into the existing Flask API.       |
|**9**| Add complete button |✅Done| - Complet button using PUT, and not deleting it|
|**10**| SMALL MILESTONE TO BASIC APP REACHED YAYAYAYYYY!!!|                   

## Prerequisites

To run this project locally, you will need:

- **Python** (3.x recommended)
- **Node.js** and **npm** (or **yarn** if preferred)
- **Flask** and required Python libraries
- **React** (frontend framework)

---

## Setup Instructions

### Backend (Flask)

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up the Python environment**:
   
   You can use `virtualenv` or `conda` for a virtual environment (optional but recommended).

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   
   Install the required Python dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**:
   
   Start the Flask development server:

   ```bash
   python app.py
   ```

   The server will run at `http://127.0.0.1:5000/`.

### Frontend (React)

1. **Install Dependencies**:
   
   Inside the `client` (or `frontend`) directory, install the necessary Node.js packages:

   ```bash
   cd client
   npm install
   ```

2. **Run the React Application**:

   Start the React development server:

   ```bash
   npm start
   ```

   The React application will run at `http://localhost:3000/`.

---

## Usage

1. **Open the React app**:
   Visit `http://localhost:3000` to view and interact with the ToDo list.

2. **Add a Task**:
   - Enter a task description, priority, category, and deadline.
   - Submit the task to add it to the list. It will be sent to the Flask backend and saved in the JSON file.

3. **View Tasks**:
   - The ToDo list will display all tasks, including descriptions, priorities, categories, and deadlines.

4. **Delete/Complete a Task**:
   - Use the appropriate button in the task list to either delete or mark a task as completed.

---

## Project Structure

Here's an overview of the key files and folders:

- **app.py**: The main Flask application.
- **todo.py**: Contains the core logic for managing tasks (adding, deleting, etc.).
- **public/**: React frontend code.
- **components/**: Contains React components such as `ToDoForm` and `ToDoList`.
- **tasks.json**: File used to persist tasks.

---

## API Endpoints

The Flask backend exposes several API endpoints for managing tasks:

- `GET /api/tasks`: Fetch all tasks.
- `POST /api/tasks`: Add a new task.
- `DELETE /api/tasks/<task_id>`: Delete a task.
- `PUT /api/tasks/<task_id>/complete`: Mark a task as completed.

---

## Troubleshooting

### CORS Issues

If you're running React and Flask on different ports (React on `3000`, Flask on `5000`), ensure that **CORS** is properly configured in your Flask app.

- Install CORS for Flask:

  ```bash
  pip install flask-cors
  ```

- Add this to your `app.py`:

  ```python
  from flask_cors import CORS
  CORS(app)
  ```

---

## Future Improvements
Improve the Frontend Design:

Refine the UI/UX for a more modern and intuitive interface.
Add responsiveness so that the app works well on mobile and tablet devices.
Implement better visual feedback for task creation, deletion, and completion.
Use a UI library like Material-UI, Bootstrap, or TailwindCSS for better styling and consistency.
Add animations or transitions when tasks are added, deleted, or marked as complete to improve the user experience.
Task Filtering and Sorting:

Allow users to filter tasks by category, priority, or completion status.
Add sorting functionality, so users can order tasks by deadline, priority, or date added.
Improved Form Validation:

Add more comprehensive validation (e.g., make sure the deadline is in the future, or all required fields are filled).
Provide error messages directly on the form when validation fails.
Accessibility:

Ensure the application is fully accessible, following web accessibility standards (e.g., WCAG).
Implement keyboard navigation and screen reader compatibility.





