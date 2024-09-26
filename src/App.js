import { useState, useEffect } from "react";
import ToDoForm from "./components/ToDoForm";
import ToDoList from "./components/ToDoList";
import ToDoCalendar from "./components/ToDoCalendar";
import TaskCategory from "./components/TaskCategory";

function App() {
  const [tasks, setTasks] = useState([]);
  const [filteredTasks, setFilteredTasks] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null); // For calendar filtering
  const [selectedCategory, setSelectedCategory] = useState(""); // For category filtering

  // Fetch tasks from Flask API on load
  useEffect(() => {
    fetch("/tasks")
      .then((res) => res.json())
      .then((data) => {
        setTasks(data);
        setFilteredTasks(data); // Initialize filtered tasks to show all initially
      });
  }, []);

  // Add task via API
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

  // Delete task via API
  const deleteTask = async (taskId) => {
    await fetch(`/tasks/${taskId}`, {
      method: "DELETE",
    });
    setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
  };

  // Mark task as complete via API
  const completeTask = async (taskId) => {
    await fetch(`/tasks/${taskId}/complete`, {
      method: "PUT",
    });
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === taskId ? { ...task, completed: true } : task
      )
    );
  };

  // Function to filter tasks by date and category
  const filterTasks = () => {
    let filtered = tasks;

    // Filter by date if a date is selected
    if (selectedDate) {
      filtered = filtered.filter((task) => {
        const taskDate = new Date(task.deadline);
        return taskDate.toDateString() === selectedDate.toDateString();
      });
    }

    // Filter by category if a category is selected
    if (selectedCategory) {
      filtered = filtered.filter((task) => task.category === selectedCategory);
    }

    setFilteredTasks(filtered); // Update the filtered task list
  };

  // UseEffect to filter tasks when either date or category changes
  useEffect(() => {
    filterTasks();
  }, [selectedDate, selectedCategory, tasks]);

  return (
    <div className="App">
      <h1>ToDo List</h1>
      {/* Task Form */}
      <ToDoForm addTask={addTask} />

      {/* Calendar for filtering tasks by deadline */}
      <ToDoCalendar onDateChange={setSelectedDate} />

      {/* Category dropdown for filtering tasks by category */}
      <TaskCategory category={selectedCategory} onCategoryChange={setSelectedCategory} />

      {/* Display the filtered tasks */}
      <ToDoList tasks={filteredTasks} deleteTask={deleteTask} completeTask={completeTask} />
    </div>
  );
}

export default App;
