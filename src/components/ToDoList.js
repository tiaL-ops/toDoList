import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { Container, Typography, Card, CardContent, CardActions, Button, Grid, MenuItem, Select, FormControl, InputLabel, TextField } from '@mui/material';
import { format, isBefore, isToday, differenceInDays } from 'date-fns';  // Date manipulation functions

const ToDoList = () => {
  const [tasks, setTasks] = useState([]); // Tasks state
  const [selectedTask, setSelectedTask] = useState(null); // Selected task state for actions
  const [sortBy, setSortBy] = useState('deadline'); // Sorting state (default is deadline)
  const [filterDate, setFilterDate] = useState(null); // Date filter state

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
      const dateA = a.deadline ? new Date(a.deadline) : new Date(9999, 11, 31); // Handle missing deadlines
      const dateB = b.deadline ? new Date(b.deadline) : new Date(9999, 11, 31);
      return dateA - dateB; // Sort by deadline
    } else {
      return 0;
    }
  });

  // Filter by selected date
  const filteredTasks = filterDate
    ? sortedTasks.filter(task => task.deadline && isBefore(new Date(task.deadline), filterDate))
    : sortedTasks;

  // Visual cues for urgency based on deadline
  const getDeadlineStatus = (deadline) => {
    if (!deadline) return '#fff3e0'; // No deadline
    const deadlineDate = new Date(deadline);
    if (isToday(deadlineDate)) return '#ffeb3b'; // Yellow if due today
    if (differenceInDays(deadlineDate, new Date()) < 3) return '#ff9800'; // Orange if due in 3 days
    if (isBefore(deadlineDate, new Date())) return '#f44336'; // Red if overdue
    return '#e0f7fa'; // Default
  };

  // Handle date change and clearing
  const handleDateChange = (event) => {
    const dateValue = event.target.value;
    if (dateValue) {
      setFilterDate(new Date(dateValue));  // Set filter date if a date is selected
    } else {
      setFilterDate(null);  // Reset filter date if cleared
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

      {/* Date filter input */}
      <TextField
        label="Filter by deadline"
        type="date"
        value={filterDate ? format(filterDate, 'yyyy-MM-dd') : ''}
        onChange={handleDateChange}  // Call handleDateChange on date change
        InputLabelProps={{
          shrink: true,
        }}
        fullWidth
        style={{ marginBottom: '20px' }}
      />

      {/* Render sorted and filtered tasks */}
      <Grid container spacing={3}>
        {filteredTasks
          .filter(task => !task.completed) // Only show incomplete tasks
          .map((task, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card 
                onClick={() => handleTaskClick(task.id)}
                sx={{
                  backgroundColor: sortBy === 'deadline' ? getDeadlineStatus(task.deadline) : '#fff3e0',
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
                    Deadline: {task.deadline ? format(new Date(task.deadline), 'MM/dd/yyyy') : 'No deadline'}
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
