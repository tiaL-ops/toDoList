# **ToDo List Application**

## **Project Overview**
This is a full-stack **ToDo List application** that allows users to manage tasks efficiently with a secure and dynamic user interface. The application uses **React** for the frontend and **Flask** for the backend, ensuring a smooth user experience while providing **JWT-based authentication** for user access control. Tasks are stored in an **SQLite** database, and real-time updates are facilitated via **Socket.IO**.

---

## **Features**
- **Task Management**: Users can create, update, delete, and complete tasks. Tasks are categorized by priority, deadlines, and status (completed/incomplete).
- **User Authentication**: Secure **JWT-based login and registration** ensures user-specific task management.
- **Persistent Data**: User tasks are stored and retrieved using **SQLite**, ensuring data persists across sessions.
- **Real-time Updates**: Task updates are broadcast to the user in real-time using **Socket.IO**.
- **Responsive UI**: The interface is responsive and user-friendly, ensuring a consistent experience across devices.

---

## **Technical Highlights**

### **Authentication with JWT**
- **JWT Authentication** ensures that users can securely register, log in, and manage their tasks. The app stores the JWT token in `localStorage` and includes it in API requests for task management.
- Each user's tasks are **scoped by their JWT token**, ensuring that only the logged-in user can view or modify their tasks.

### **Task Operations**
- **CRUD Operations** (Create, Read, Update, Delete) on tasks are secured using the **JWT token** to ensure only authenticated users can interact with their own tasks.
- **Task Assignment**: Tasks are assigned to the currently logged-in user and filtered based on their authentication token. Users can only view and manage their own tasks.

### **Real-time Updates with Socket.IO**
- **Real-time Task Updates**: Whenever a task is added, edited, or deleted, real-time updates are pushed to the user using **Socket.IO** for instant feedback.
  
---

## **Recent Fixes**

- **Fixed Login/Registration Flow**: Resolved the login and registration issue by ensuring that user credentials are handled securely and tasks are correctly scoped to each user via JWT.
- **Fixed Task Ownership**: Now tasks are tied to specific users based on their JWT token, ensuring that users can only view and manage their own tasks.
  
---

## **Technologies Used**
- **Frontend**: React, CSS
- **Backend**: Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Migrate
- **Database**: SQLite
- **Real-time**: Socket.IO
- **Authentication**: JSON Web Tokens (JWT) for secure login and access control

---

## **How to Run the Project**

### **Backend (Flask)**

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
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



