import React, { useState } from 'react';

const ToDoForm = () => {
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('Medium');
  const [category, setCategory] = useState('General');
  const [deadline, setDeadline] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();

    const taskData = {
      description,
      priority,
      category,
      deadline
    };
    
    console.log('Submitting task:', taskData);
    fetch('http://127.0.0.1:5000/api/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Success:', data);
        // Clear the form after successful submission
        setDescription('');
        setPriority('Medium');
        setCategory('General');
        setDeadline('');
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Task description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      />
      <input
        type="date"
        value={deadline}
        onChange={(e) => setDeadline(e.target.value)}
      />
      <button type="submit">Add Task</button>
    </form>
  );
};

export default ToDoForm;
