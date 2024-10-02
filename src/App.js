import { useState, useEffect } from "react";
import ToDoForm from "./components/ToDoForm";
import ToDoList from "./components/ToDoList";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegistrationForm"; 

function App() {
  const [tasks, setTasks] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [showLogin, setShowLogin] = useState(true);  // State to toggle between login and register forms

  useEffect(() => {
    // Fetch tasks from the Flask API only if authenticated
    if (token) {
      fetch("/api/tasks", {
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          setTasks(data.tasks);
        })
        .catch((error) => {
          console.error("Error fetching tasks:", error);
          // Handle token expiration or invalid token
          if (error.status === 401) {
            setIsAuthenticated(false);
            localStorage.removeItem('token');
          }
        });
    }
  }, [token]);

  // Handle login
  const handleLogin = async (credentials) => {
    const response = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    });

    if (response.ok) {
      const data = await response.json();
      const jwtToken = data.access_token;

      // Store the token and update the state
      localStorage.setItem('token', jwtToken);
      setToken(jwtToken);
      setIsAuthenticated(true);
    } else {
      console.error("Login failed");
    }
  };

  const handleRegister = async (credentials) => {
    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });
  
      const data = await response.json();
      if (response.ok) {
        console.log('Registration successful:', data);
      } else {
        console.error('Registration failed:', data);
      }
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };
  handleRegister({ username: 'testuser', password: 'testpassword' });
  
  const handleLogout = () => {
    // Clear token from localStorage and reset state
    localStorage.removeItem('token');
    setToken(null);
    setIsAuthenticated(false);
    setTasks([]);
  };

  const addTask = async (task) => {
    const response = await fetch("/api/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify(task),
    });

    if (response.ok) {
      const newTask = await response.json();
      setTasks((prevTasks) => [...prevTasks, newTask]);
    } else {
      console.error("Failed to add task");
    }
  };

  const deleteTask = async (taskId) => {
    const response = await fetch(`/api/tasks/${taskId}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    if (response.ok) {
      setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
    } else {
      console.error("Failed to delete task");
    }
  };

  const completeTask = async (taskId) => {
    const response = await fetch(`/tasks/${taskId}/complete`, {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    if (response.ok) {
      setTasks((prevTasks) =>
        prevTasks.map((task) =>
          task.id === taskId ? { ...task, completed: true } : task
        )
      );
    } else {
      console.error("Failed to complete task");
    }
  };

  const editTask = async (taskId, editedTask) => {
    const updatedTask = {
      description: editedTask.description,
      priority: editedTask.priority,
      category: editedTask.category,
      deadline: editedTask.deadline,
    };

    const response = await fetch(`/api/tasks/${taskId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify(updatedTask),
    });

    if (response.ok) {
      const updatedTaskFromServer = await response.json();
      setTasks((prevTasks) =>
        prevTasks.map((task) =>
          task.id === taskId ? updatedTaskFromServer.task : task
        )
      );
    } else {
      console.error("Failed to update task");
    }
  };

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
                <button onClick={() => setShowLogin(false)}>
                  Register
                </button>
              </p>
            </>
          ) : (
            <>
              <RegisterForm onRegister={handleRegister} />
              <p>
                Already have an account?{" "}
                <button onClick={() => setShowLogin(true)}>
                  Login
                </button>
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
const testFetch = async () => {
  try {
    const response = await fetch(`http://localhost:5000/test`, {
      method: "GET",
    });
    const data = await response.json();
    console.log("Test Fetch Response:", data);
  } catch (error) {
    console.error("Test fetch failed:", error);
  }
};

useEffect(() => {
  testFetch();  // Call this to see if the server is responding
}, []);

export default App;
