import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { Container, Typography, Card, CardContent, CardActions, Button, Grid, MenuItem, Select, FormControl, InputLabel } from '@mui/material';

const ToDoList = () => {
  const [tasks, setTasks] = useState([]); // Tasks state
  const [selectedTask, setSelectedTask] = useState(null); // Selected task state for actions
  const [sortBy, setSortBy] = useState('priority'); // Sorting state (default is priority)

  // Priority levels mapping
  const priorityLevels = { 'High': 1, 'Medium': 2, 'Low': 3 };

  // Fetch tasks and setup WebSocket
  useEffect(() => {
    const socket = io('http://127.0.0.1:5000');

    fetch('http://127.0.0.1:5000/api/tasks')
      .then(response => response.json())
      .then(data => setTasks(data.tasks)) // Set the fetched tasks
      .catch(error => console.error('Error fetching tasks:', error));

    // Socket events for real-time task updates
    socket.on('task_update', (newTask) => {
      setTasks(prevTasks => [...prevTasks, newTask]); // Add the new task to the existing list
    });

    socket.on('task_deleted', ({ task_id }) => {
      setTasks(prevTasks => prevTasks.filter(task => task.id !== task_id)); // Remove the deleted task
    });

    return () => {
      socket.disconnect(); // Cleanup socket connection on component unmount
    };
  }, []);

  // Handle task completion
  const completeTask = (task_id) => {
    fetch(`http://127.0.0.1:5000/tasks/${task_id}/complete`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        setTasks(prevTasks => prevTasks.filter(task => task.id !== task_id)); // Filter out completed task
      })
      .catch(error => console.error('Error completing task:', error));
  };

  // Handle task deletion
  const deleteTask = (task_id) => {
    fetch(`http://127.0.0.1:5000/api/tasks/${task_id}`, { method: 'DELETE' })
      .then(response => response.json())
      .then(data => {
        setTasks(prevTasks => prevTasks.filter(task => task.id !== task_id)); // Filter out deleted task
      })
      .catch(error => console.error('Error deleting task:', error));
  };

  // Handle task click (toggle selection for actions)
  const handleTaskClick = (task_id) => {
    setSelectedTask(task_id === selectedTask ? null : task_id); // Toggle selected task
  };

  // Handle sort change
  const handleSortChange = (event) => {
    setSortBy(event.target.value); 
  };

  // Sorting logic (runs every render)
  const sortedTasks = tasks.slice().sort((a, b) => {
    if (sortBy === 'priority') {
      return priorityLevels[a.priority] - priorityLevels[b.priority]; // Sort by priority (High > Medium > Low)
    } else if (sortBy === 'deadline') {
      const dateA = a.deadline ? new Date(a.deadline) : new Date(9999, 11, 31); 
      const dateB = b.deadline ? new Date(b.deadline) : new Date(9999, 11, 31);
      return dateA - dateB; // Sort by deadline
    } else {
      return 0;
    }
  });

  // Get the background color based on priority
  const getCardBackgroundColor = (priority) => {
    switch (priority) {
      case 'High':
        return '#f44336'; // Red for high priority
      case 'Medium':
        return '#ff9800'; // Orange for medium priority
      case 'Low':
        return '#ffeb3b'; // Yellow for low priority
      default:
        return '#ffffff'; // Default white background
    }
  };

  return (
    <Container>
      <Typography variant="h4" align="center" gutterBottom>
        My To-Do List
      </Typography>

      {/* Sorting Dropdown */}
      <FormControl fullWidth style={{ marginBottom: '20px' }}>
        <InputLabel id="sort-by-label">Sort By</InputLabel>
        <Select
          labelId="sort-by-label"
          id="sort-by"
          value={sortBy}
          label="Sort By"
          onChange={handleSortChange} 
        >
          <MenuItem value="priority">Priority</MenuItem>
          <MenuItem value="deadline">Deadline</MenuItem>
        </Select>
      </FormControl>

      {/* Render sorted tasks */}
      <Grid container spacing={3}>
        {sortedTasks
          .filter(task => !task.completed) // Only show incomplete tasks
          .map((task, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card 
                onClick={() => handleTaskClick(task.id)}
                sx={{
                  backgroundColor: sortBy === 'priority' ? getCardBackgroundColor(task.priority) : '#fff3e0',
                  cursor: 'pointer',
                  ':hover': { boxShadow: '0 5px 15px rgba(0,0,0,0.3)' }
                }}
              >
                <CardContent>
                  <Typography variant="h6">{task.description}</Typography>
                  <Typography variant="body2" color="textSecondary">
                    Priority: {task.priority}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Category: {task.category}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Deadline: {task.deadline ? task.deadline : 'No deadline'}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Status: {task.completed ? "Completed" : "Pending"}
                  </Typography>
                </CardContent>
                {selectedTask === task.id && (
                  <CardActions>
                    <Button color="primary" onClick={() => completeTask(task.id)}>
                      Complete
                    </Button>
                    <Button color="secondary" onClick={() => deleteTask(task.id)}>
                      Delete
                    </Button>
                  </CardActions>
                )}
              </Card>
            </Grid>
          ))}
      </Grid>
    </Container>
  );
};

export default ToDoList;
