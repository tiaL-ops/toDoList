import React, { useState } from 'react';
import axios from 'axios';

const TodoForm = ({ addTask }) => {
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('Medium');
  const [category, setCategory] = useState('General');
  const [deadline, setDeadline] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const newTask = { description, priority, category, deadline };

    axios.post('http://127.0.0.1:5000/tasks', newTask)
      .then(response => {
        addTask(newTask);
        setDescription('');
        setPriority('Medium');
        setCategory('General');
        setDeadline('');
      })
      .catch(error => {
        console.error('There was an error adding the task!', error);
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text" 
        value={description} 
        onChange={e => setDescription(e.target.value)} 
        placeholder="Task Description" 
        required 
      />
      <select value={priority} onChange={e => setPriority(e.target.value)}>
        <option value="Low">Low</option>
        <option value="Medium">Medium</option>
        <option value="High">High</option>
      </select>
      <input 
        type="date" 
        value={deadline} 
        onChange={e => setDeadline(e.target.value)} 
      />
      <button type="submit">Add Task</button>
    </form>
  );
};

export default TodoForm;
