# **ToDo List Application**

## **Project Overview**
This is a full-stack **ToDo List application** that allows users to create, view, manage, and organize tasks. It features a **React frontend** for a dynamic user interface and a **Flask backend** for handling task management, authentication, and persistence using **SQLite**. The app showcases how to build and connect a frontend and backend system, with a focus on **modern web development** practices such as **JWT authentication** and **real-time updates**.

---

## **Features**
- **Task Management**: Create, update, delete, and complete tasks, with priorities, deadlines, and categories.
- **User Authentication**: Secure login system using **JWT tokens** for authentication and access control.
- **Persistent Storage**: Tasks are stored using **SQLite** for long-term storage and retrieval.
- **Responsive UI**: Designed to work smoothly on both desktop and mobile devices using modern frontend technologies.

---

## **Current Status & Bug**
### **Current Bug**
I'm currently debugging the **login functionality** where attempting to log in via the `/login` endpoint returns a `500 Internal Server Error`. The issue seems to occur when querying for the user in the database. 

### **Steps Taken to Debug the Login Issue**
1. **Checked Flask Logs**: Found a `NoneType` error when querying for the user in the database.
2. **Verified User in the Database**:
   - Used Flask shell to check if the user existed: `User.query.filter_by(username="testuser").first()`.
   - Discovered the user did not exist.
3. **Added a New User**:
   - Created the user manually in the database with a hashed password using Flask shell.
4. **Re-tested Login**:
   - The login still returned a `500 Internal Server Error`. More logging was added to troubleshoot further.
   
---

## **Technologies Used**
- **Frontend**: React, CSS
- **Backend**: Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **Database**: SQLite
- **Authentication**: JWT (JSON Web Tokens) for secure login and user authentication.

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

1. **Install Dependencies**:
   ```bash
   cd client
   npm install
   ```

2. **Start the React Application**:
   ```bash
   npm start
   ```

---

## **API Endpoints**
- `POST /login`: Authenticate user and issue JWT token.
- `GET /api/tasks`: Retrieve tasks (requires valid JWT).
- `POST /api/tasks`: Create a new task (requires valid JWT).

---

## **Future Plans**
- **Fix Login Issue**: Resolve the `500 Internal Server Error` and ensure smooth user authentication.
- **Enhance User Experience**: Improve the UI with better animations and real-time task updates.
- **Add Notifications**: Push notifications for task deadlines.

---

## **Conclusion**
This project has been a journey of building a full-stack application using Flask and React. While there have been challenges, such as the current login issue, I am continuously learning and improving the app as I progress.
