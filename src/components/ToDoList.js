import React, { useState, useEffect } from 'react';

const ToDoList = () => {
  const [tasks, setTasks] = useState([]);

  // Fetch tasks when the component mounts
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/tasks')  // Full URL for Flask API
      .then(response => response.json())
      .then(data => {
        setTasks(data.tasks);  // Make sure data.tasks is correctly accessed
      })
      .catch(error => console.error('Error fetching tasks:', error));
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
