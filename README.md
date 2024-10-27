# **ToDo List Application**

## **Project Overview**
This is my first full-stack **ToDo List application**, built as a personal project to explore and learn **Python** and **React**. Throughout this project, I aimed to understand the basics of full-stack development, tackle challenges like **authentication**, **real-time updates**, and **deployment**, and experience the full development cycle from scratch.

The application allows users to manage tasks with a secure, interactive interface, using **React** for the frontend and **Flask** for the backend. User sessions are protected with **JWT-based authentication**, while tasks are stored in an **SQLite** database and updated in real-time with **Socket.IO**.

> **Note**: This project might be messy, as it was my first venture into the world of full-stack development. I learned so much through trial and error, and I’m excited to apply these lessons in future, cleaner projects! 

---

## **Features**
- **Task Management**: Users can create, update, delete, and complete tasks, organized by priority, deadlines, and status.
- **User Authentication**: Secure **JWT-based login and registration** ensures that each user's tasks are private and accessible only to them.
- **Persistent Data**: User tasks are saved in **SQLite** to maintain data across sessions.
- **Real-time Updates**: Task changes are instantly pushed to the user’s interface using **Socket.IO**.
- **Responsive UI**: The app is optimized for different screen sizes to ensure a consistent user experience.

---

## **Personal Reflections and Learnings**

### **Learning Full-Stack Development**
This project taught me how to set up and connect a backend and frontend. I learned how to structure **React** components and manage backend routes with **Flask**. I also explored how to securely authenticate users and manage their sessions with **JWT**.

### **Discovering Development and Rookies mistake :D ** 
Being my first project, I encountered and overcame many issues with file organization, environment configuration, and deployment. Here are a few highlights:
- **`.gitignore` and `.env` Files**: I learned to exclude sensitive information and large files from Git.
- **Organizing Code**: Understanding how to separate concerns and organize code has been crucial,
- **Deployment Challenges**: Learned how organization affect deployment highly

---

## **Technical Highlights**

### **Skills and Technologies Used**
- **Frontend**: React, CSS for styling, responsiveness.
- **Backend**: Flask, Flask-SQLAlchemy for ORM, Flask-JWT-Extended for authentication, Flask-Migrate for database migrations.
- **Database**: SQLite, selected for simplicity in this personal project.
- **Real-time Features**: Socket.IO for instant task updates.
- **Authentication**: JSON Web Tokens (JWT) for secure user login and access control.

### **Authentication with JWT**
- Users register and log in using **JWT authentication**, with tokens stored in `localStorage` for persistent sessions.
- Each user's tasks are scoped by their JWT token, ensuring data privacy and security.

### **Task Operations**
- Full **CRUD Operations** (Create, Read, Update, Delete) on tasks, secured with JWT to ensure only authenticated users can access or manage their tasks.
- Tasks are assigned to the logged-in user and filtered based on the authentication token.

### **Real-time Updates with Socket.IO**
- Task updates are broadcast in real-time using **Socket.IO**, providing instant feedback for task changes.

---

## **How to Run the Project**

### **Backend (Flask)**

1. **Clone the Repository**:
   ```bash
   git clone <https://github.com/tiaL-ops/toDoList.git>
   cd <my-todo-app>
   ```

2. **Set up the Python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask Server**:
   ```bash
   flask run
   ```

### **Frontend (React)**

1. **Navigate to the frontend directory**:
   ```bash
   cd client
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Start the React Application**:
   ```bash
   npm start
   ```

---

## **API Endpoints**

- `POST /register`: Register a new user.
- `POST /login`: Authenticate user and issue JWT token.
- `GET /api/tasks`: Retrieve tasks for the authenticated user (requires valid JWT).
- `POST /api/tasks`: Create a new task (requires valid JWT).
- `PUT /api/tasks/<task_id>`: Edit a specific task (requires valid JWT).
- `DELETE /api/tasks/<task_id>`: Delete a specific task (requires valid JWT).
- `PUT /tasks/<task_id>/complete`: Mark a task as complete (requires valid JWT).

---

## **Moving Forward**

Completing this project has been a fantastic learning experience. Although it may look a bit messy, it represents my initial steps into full-stack development, building skills in **React**, **Flask**, **JWT authentication**, **Socket.IO**, and **database management**.


---

