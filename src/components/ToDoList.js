import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TodoList = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/tasks')
      .then(response => {
        setTasks(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the tasks!', error);
      });
  }, []);

  const handleComplete = (taskId) => {
    axios.put(`http://127.0.0.1:5000/tasks/${taskId}/complete`)
      .then(response => {
        setTasks(tasks.map(task => 
          task.id === taskId ? { ...task, completed: true } : task
        ));
      })
      .catch(error => {
        console.error('There was an error marking the task complete!', error);
      });
  };

  const handleDelete = (taskId) => {
    axios.delete(`http://127.0.0.1:5000/tasks/${taskId}`)
      .then(response => {
        setTasks(tasks.filter(task => task.id !== taskId));
      })
      .catch(error => {
        console.error('There was an error deleting the task!', error);
      });
  };

  return (
    <div className="todo-list">
      <h2>My To-Do List</h2>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>
            <span style={{ textDecoration: task.completed ? 'line-through' : 'none' }}>
              {task.description} ({task.priority})
            </span>
            <button onClick={() => handleComplete(task.id)}>Complete</button>
            <button onClick={() => handleDelete(task.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
