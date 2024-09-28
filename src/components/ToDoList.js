import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { Container, Typography, Card, CardContent, CardActions, Button, Grid, MenuItem, Select, FormControl, InputLabel, TextField } from '@mui/material';
import { format, isBefore, isToday, differenceInDays } from 'date-fns';

const ToDoList = () => {
  const [tasks, setTasks] = useState([]); // Tasks state
  const [selectedTask, setSelectedTask] = useState(null); // Selected task state for actions
  const [isEditing, setIsEditing] = useState(null); // State to track which task is being edited
  const [editedTask, setEditedTask] = useState(null); // Track the changes for the task being edited
  const [sortBy, setSortBy] = useState('deadline'); // Sorting state (default is deadline)
  const [filterDate, setFilterDate] = useState(null); // Date filter state
  const [showCompleted, setShowCompleted] = useState('incomplete'); // Filter for viewing incomplete, completed, or all tasks

  const priorityLevels = { 'High': 1, 'Medium': 2, 'Low': 3 };

  useEffect(() => {
    const socket = io('http://127.0.0.1:5000');

    fetch('http://127.0.0.1:5000/api/tasks')
      .then(response => response.json())
      .then(data => setTasks(data.tasks))
      .catch(error => console.error('Error fetching tasks:', error));

    // Handle task updates via socket
    socket.on('task_update', (updatedTask) => {
      setTasks(prevTasks => {
        
        const taskExists = prevTasks.find(task => task.id === updatedTask.id);
        if (taskExists) {
          return prevTasks.map(task => task.id === updatedTask.id ? updatedTask : task);
        }
        return [...prevTasks, updatedTask];
      });
    });

    // Handle task deletion via socket
    socket.on('task_deleted', ({ task_id }) => {
      setTasks(prevTasks => prevTasks.filter(task => task.id !== task_id));
    });

    return () => {
      socket.disconnect();
    };
  }, []);

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
        setTasks(prevTasks => 
          prevTasks.map(task => 
            task.id === task_id ? { ...task, completed: true } : task
          )
        );
      })
      .catch(error => console.error('Error completing task:', error));
  };

  const deleteTask = (task_id) => {
    fetch(`http://127.0.0.1:5000/api/tasks/${task_id}`, { method: 'DELETE' })
      .then(response => response.json())
      .then(data => {
        setTasks(prevTasks => prevTasks.filter(task => task.id !== task_id));
      })
      .catch(error => console.error('Error deleting task:', error));
  };

  const handleTaskClick = (task_id) => {
    setSelectedTask(task_id === selectedTask ? null : task_id);
  };

  const handleSortChange = (event) => {
    setSortBy(event.target.value);
  };

  const handleShowCompletedChange = (event) => {
    setShowCompleted(event.target.value);
  };

  const handleEditClick = (task) => {
    setIsEditing(task.id);
    setEditedTask({ ...task }); // Preload the editing form with the existing task details
  };

  const handleEditChange = (event) => {
    const { name, value } = event.target;
    setEditedTask(prev => ({ ...prev, [name]: value }));
  };

  const saveEditedTask = (task_id) => {
    fetch(`http://127.0.0.1:5000/api/tasks/${task_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editedTask)
    })
      .then(response => response.json())
      .then(updatedTask => {
        setTasks(prevTasks => prevTasks.map(task => task.id === task_id ? updatedTask.task : task)); // Ensure correct update of task
        setIsEditing(null);
      })
      .catch(error => console.error('Error editing task:', error));
  };

  const sortedTasks = tasks.slice().sort((a, b) => {
    if (sortBy === 'priority') {
      return priorityLevels[a.priority] - priorityLevels[b.priority];
    } else if (sortBy === 'deadline') {
      const dateA = a.deadline ? new Date(a.deadline) : new Date(9999, 11, 31);
      const dateB = b.deadline ? new Date(b.deadline) : new Date(9999, 11, 31);
      return dateA - dateB;
    } else {
      return 0;
    }
  });

  const filteredTasks = sortedTasks.filter(task => {
    const matchesDateFilter = filterDate
      ? task.deadline && isBefore(new Date(task.deadline), filterDate)
      : true;

    const matchesCompletedFilter = 
      (showCompleted === 'incomplete' && !task.completed) ||
      (showCompleted === 'completed' && task.completed) ||
      showCompleted === 'all';

    return matchesDateFilter && matchesCompletedFilter;
  });

  const getCardBackgroundColor = (task) => {
    if (task.completed) {
      return '#4caf50'; // Green for completed tasks
    } else if (sortBy === 'priority') {
      switch (task.priority) {
        case 'High':
          return '#f44336'; // Red for high priority
        case 'Medium':
          return '#ff9800'; // Orange for medium priority
        case 'Low':
          return '#ffeb3b'; // Yellow for low priority
        default:
          return '#ffffff'; // Default white background
      }
    } else if (sortBy === 'deadline') {
      return getDeadlineStatus(task.deadline);
    } else {
      return '#ffffff';
    }
  };

  const getDeadlineStatus = (deadline) => {
    if (!deadline) return '#fff3e0';
    const deadlineDate = new Date(deadline);
    if (isToday(deadlineDate)) return '#ffeb3b';
    if (differenceInDays(deadlineDate, new Date()) < 3) return '#ff9800';
    if (isBefore(deadlineDate, new Date())) return '#f44336';
    return '#e0f7fa';
  };

  const handleDateChange = (event) => {
    const dateValue = event.target.value;
    if (dateValue) {
      setFilterDate(new Date(dateValue));
    } else {
      setFilterDate(null);
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

      {/* View Completed/Incomplete Toggle */}
      <FormControl fullWidth style={{ marginBottom: '20px' }}>
        <InputLabel id="show-completed-label">Show Tasks</InputLabel>
        <Select
          labelId="show-completed-label"
          id="show-completed"
          value={showCompleted}
          label="Show Tasks"
          onChange={handleShowCompletedChange}
        >
          <MenuItem value="incomplete">Incomplete Tasks</MenuItem>
          <MenuItem value="completed">Completed Tasks</MenuItem>
          <MenuItem value="all">All Tasks</MenuItem>
        </Select>
      </FormControl>

      {/* Date filter input */}
      <TextField
        label="Filter by deadline"
        type="date"
        value={filterDate ? format(filterDate, 'yyyy-MM-dd') : ''}
        onChange={handleDateChange}
        InputLabelProps={{
          shrink: true,
        }}
        fullWidth
        style={{ marginBottom: '20px' }}
      />

      {/* Render sorted and filtered tasks */}
      <Grid container spacing={3}>
        {filteredTasks.map((task, index) => (
          <Grid item xs={12} sm={6} md={4} key={task.id}> {/* Ensure unique key */}
            <Card 
              onClick={() => handleTaskClick(task.id)}
              sx={{
                backgroundColor: getCardBackgroundColor(task),
                cursor: 'pointer',
                ':hover': { boxShadow: '0 5px 15px rgba(0,0,0,0.3)' }
              }}
            >
              {isEditing === task.id ? (
                <CardContent>
                  <TextField
                    label="Description"
                    value={editedTask.description}
                    name="description"
                    onChange={handleEditChange}
                    fullWidth
                    style={{ marginBottom: '10px' }}
                  />
                  <FormControl fullWidth style={{ marginBottom: '10px' }}>
                    <InputLabel id="edit-priority-label">Priority</InputLabel>
                    <Select
                      labelId="edit-priority-label"
                      value={editedTask.priority}
                      name="priority"
                      onChange={handleEditChange}
                    >
                      <MenuItem value="High">High</MenuItem>
                      <MenuItem value="Medium">Medium</MenuItem>
                      <MenuItem value="Low">Low</MenuItem>
                    </Select>
                  </FormControl>
                  <TextField
                    label="Deadline"
                    type="date"
                    value={editedTask.deadline ? format(new Date(editedTask.deadline), 'yyyy-MM-dd') : ''}
                    name="deadline"
                    onChange={handleEditChange}
                    InputLabelProps={{
                      shrink: true,
                    }}
                    fullWidth
                    style={{ marginBottom: '10px' }}
                  />
                  <TextField
                    label="Category"
                    value={editedTask.category}
                    name="category"
                    onChange={handleEditChange}
                    fullWidth
                  />
                </CardContent>
              ) : (
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
              )}
              {selectedTask === task.id && (
                <CardActions>
                  {!task.completed && isEditing !== task.id && (
                    <Button color="primary" onClick={() => completeTask(task.id)}>
                      Complete
                    </Button>
                  )}
                  {isEditing === task.id ? (
                    <Button color="primary" onClick={() => saveEditedTask(task.id)}>
                      Save
                    </Button>
                  ) : (
                    <Button color="primary" onClick={() => handleEditClick(task)}>
                      Edit
                    </Button>
                  )}
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
