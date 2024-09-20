import React, { useState } from 'react';

const AddTaskForm = ({ onTaskAdded }) => {
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('Medium');
  const [category, setCategory] = useState('General');
  const [deadline, setDeadline] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const newTask = {
      description,
      priority,
      category,
      deadline
    };

    // Send the task to the Flask API
    fetch('http://127.0.0.1:5000/api/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTask),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Task added:', data);
        if (onTaskAdded) onTaskAdded();  // Notify parent component to refresh the task list if needed
      })
      .catch((error) => console.error('Error adding task:', error));

    // Clear the form fields
    setDescription('');
    setPriority('Medium');
    setCategory('General');
    setDeadline('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="text"
          placeholder="Task description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
      </div>
      <div>
        <select value={priority} onChange={(e) => setPriority(e.target.value)}>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>
      <div>
        <input
          type="text"
          placeholder="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
      </div>
      <div>
        <input
          type="date"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
        />
      </div>
      <button type="submit">Add Task</button>
    </form>
  );
};

export default AddTaskForm;
