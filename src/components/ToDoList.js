import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';  // Import socket.io-client

const ToDoList = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    
    const socket = io('http://127.0.0.1:5000');

    // Fetch initial tasks from REST API
    fetch('http://127.0.0.1:5000/api/tasks')
      .then(response => response.json())
      .then(data => setTasks(data.tasks))
      .catch(error => console.error('Error fetching tasks:', error));

    // Listen for new task updates
    socket.on('task_update', (newTask) => {
      setTasks(prevTasks => [...prevTasks, newTask]);  // Add new task to task list
    });

    // Listen for task deletion
    socket.on('task_deleted', ({ task_id }) => {
      setTasks(prevTasks => prevTasks.filter((task, index) => index !== task_id));
    });

    // Listen for task completion
    socket.on('task_completed', ({ task_id }) => {
      setTasks(prevTasks => prevTasks.map((task, index) =>
        index === task_id ? { ...task, completed: true } : task
      ));
    });

    // Cleanup WebSocket connection on component unmount
    return () => {
      socket.disconnect();
    };
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
