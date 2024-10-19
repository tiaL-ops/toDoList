import React, { useState } from 'react';

const ToDoForm = () => {
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('Medium');
  const [category, setCategory] = useState('General');
  const [deadline, setDeadline] = useState('');
  
  // Retrieve token from localStorage
  const token = localStorage.getItem('token'); 


  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Add Task button clicked. Submitting task...');
    const taskData = {
      description,
      priority,
      category,
      deadline
    };
    
    console.log('heyyyyy:', taskData);
    
    // Check if token exists
    if (!token) {
      console.error("No token found. User might not be authenticated.");
      return;
    }

    fetch('http://127.0.0.1:5000/api/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "Authorization": `Bearer ${token}`,  // Include the token in the request
      },
      body: JSON.stringify(taskData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to add task');
        }
        return response.json();
      })
      .then((data) => {
        console.log('Success: WHat', data);
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
      <div>
        <select value={priority} onChange={(e) => setPriority(e.target.value)}>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>
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
