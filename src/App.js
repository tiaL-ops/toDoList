import { useState, useEffect } from "react";
import ToDoForm from "./components/ToDoForm";
import ToDoList from "./components/ToDoList";

function App() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    // Fetch tasks from the Flask API on load
    fetch("/tasks")
      .then((res) => res.json())
      .then((data) => {
        setTasks(data);
      });
  }, []);

  const addTask = async (task) => {
    const response = await fetch("/api/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(task),
    });
    const newTask = await response.json();
    setTasks((prevTasks) => [...prevTasks, newTask]);
  };

  const deleteTask = async (taskId) => {
    await fetch(`/tasks/${taskId}`, {
      method: "DELETE",
    });
    setTasks((prevTasks) => prevTasks.filter((_, index) => index + 1 !== taskId));
  };

  const completeTask = async (taskId) => {
    await fetch(`/tasks/${taskId}/complete`, {
      method: "PUT",
    });
    setTasks((prevTasks) =>
      prevTasks.map((task, index) =>
        index + 1 === taskId ? { ...task, completed: true } : task
      )
    );
  };

  const editTask = async (taskId) => {
    // Prepare the updated task data
    const updatedTask = {
      description: editedTask.description,
      priority: editedTask.priority,
      category: editedTask.category,
      deadline: editedTask.deadline,
    };
  
    // Send the PUT request with the updated task data
  const response = await fetch(`/api/tasks/${taskId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(updatedTask),
  });

  if (response.ok) {
    const updatedTaskFromServer = await response.json();

    // Update the task in the local state correctly
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === taskId ? updatedTaskFromServer.task : task
      )
    );

    // Exit editing mode
    setIsEditing(null);
  } else {
    console.error("Failed to update task");
  }
};


  return (
    <div className="App">
      <h1>ToDo List</h1>
      <ToDoForm addTask={addTask} />
      <ToDoList tasks={tasks} deleteTask={deleteTask} completeTask={completeTask} />
    </div>
  );
}

export default App;