import { useState, useEffect } from "react";
import ToDoForm from "./components/ToDoForm";
import ToDoList from "./components/ToDoList";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegistrationForm";

function App() {
  const [tasks, setTasks] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [showLogin, setShowLogin] = useState(true);

  // Fetch tasks only when authenticated
  useEffect(() => {
    const fetchTasks = async () => {
      if (!token) return;
      
      try {
        const response = await fetch("/api/tasks", {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          if (response.status === 401) {
            setIsAuthenticated(false);
            localStorage.removeItem('token');
            return;
          }
          throw new Error(`Failed to fetch tasks: ${response.statusText}`);
        }

        const data = await response.json();
        setTasks(data.tasks);
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };

    fetchTasks();
  }, [token]);

  // Handle login
  const handleLogin = async (credentials) => {
    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) throw new Error("Login failed");

      const data = await response.json();
      const jwtToken = data.access_token;

      localStorage.setItem('token', jwtToken);
      setToken(jwtToken);
      setIsAuthenticated(true);
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  // Handle registration
  const handleRegister = async (credentials) => {
    try {
      const response = await fetch("http://localhost:5000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(`Registration failed: ${data.message}`);
      }

      console.log('Registration successful:', data);
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setIsAuthenticated(false);
    setTasks([]);
  };

  // Add a new task
  const addTask = async (task) => {
    try {
      const response = await fetch("/api/tasks", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(task),
      });

      if (!response.ok) throw new Error("Failed to add task");

      const newTask = await response.json();
      setTasks((prevTasks) => [...prevTasks, newTask]);
    } catch (error) {
      console.error("Add task error:", error);
    }
  };

  // Delete a task
  const deleteTask = async (taskId) => {
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });

      if (!response.ok) throw new Error("Failed to delete task");

      setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
    } catch (error) {
      console.error("Delete task error:", error);
    }
  };

  // Complete a task
  const completeTask = async (taskId) => {
    try {
      const response = await fetch(`/tasks/${taskId}/complete`, {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });

      if (!response.ok) throw new Error("Failed to complete task");

      setTasks((prevTasks) =>
        prevTasks.map((task) =>
          task.id === taskId ? { ...task, completed: true } : task
        )
      );
    } catch (error) {
      console.error("Complete task error:", error);
    }
  };

  // Edit a task
  const editTask = async (taskId, editedTask) => {
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(editedTask),
      });

      if (!response.ok) throw new Error("Failed to update task");

      const updatedTaskFromServer = await response.json();
      setTasks((prevTasks) =>
        prevTasks.map((task) =>
          task.id === taskId ? updatedTaskFromServer.task : task
        )
      );
    } catch (error) {
      console.error("Edit task error:", error);
    }
  };

  // Fetch test data
  useEffect(() => {
    const fetchTestData = async () => {
      try {
        const response = await fetch("http://localhost:5000/test", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) throw new Error(`Failed to fetch test data: ${response.statusText}`);

        const result = await response.json();
        console.log("Test fetch result:", result);
      } catch (error) {
        console.error("Test fetch error:", error);
      }
    };

    fetchTestData();
  }, []);

  return (
    <div className="App">
      <h1>ToDo List</h1>
      {!isAuthenticated ? (
        <>
          {showLogin ? (
            <>
              <LoginForm onLogin={handleLogin} />
              <p>
                Don't have an account?{" "}
                <button onClick={() => setShowLogin(false)}>Register</button>
              </p>
            </>
          ) : (
            <>
              <RegisterForm onRegister={handleRegister} />
              <p>
                Already have an account?{" "}
                <button onClick={() => setShowLogin(true)}>Login</button>
              </p>
            </>
          )}
        </>
      ) : (
        <>
          <button onClick={handleLogout}>Logout</button>
          <ToDoForm addTask={addTask} />
          <ToDoList
            tasks={tasks}
            deleteTask={deleteTask}
            completeTask={completeTask}
            editTask={editTask}
          />
        </>
      )}
    </div>
  );
}

export default App;
