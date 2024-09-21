import React, { useState, useEffect } from 'react';

const ToDoList = () => {
  const [tasks, setTasks] = useState([]);

  // Function to fetch tasks
  const fetchTasks = () => {
    fetch('http://127.0.0.1:5000/api/tasks')  // Full URL for Flask API
      .then(response => response.json())
      .then(data => {
        setTasks(data.tasks);  // Make sure data.tasks is correctly accessed
      })
      .catch(error => console.error('Error fetching tasks:', error));
  };

  // Fetch tasks on mount and set polling to keep it updated
  useEffect(() => {
    // Fetch tasks initially
    fetchTasks();

    // Set up polling every 5 seconds (5000 milliseconds)
    const intervalId = setInterval(fetchTasks, 5000);

    // Cleanup: Clear the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <h2>Task List</h2>
      {tasks.length > 0 ? (
        <ul>
          {tasks.map((task, index) => (
            <li key={index}>
              <strong>{task.description}</strong> 
              (Priority: {task.priority}, 
              Category: {task.category}, 
              Deadline: {task.deadline ? task.deadline : 'No deadline'}) 
              {task.completed ? " [✓]" : " [✗]"}
            </li>
          ))}
        </ul>
      ) : (
        <p>No tasks available.</p>
      )}
    </div>
  );
};

export default ToDoList;
