import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { Container, Typography, Card, CardContent, CardActions, Button, Grid } from '@mui/material';  // Import MUI components

const ToDoList = () => {
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);  // Track which task is selected

  // Fetch tasks from the backend
  useEffect(() => {
    const socket = io('http://127.0.0.1:5000');

    fetch('http://127.0.0.1:5000/api/tasks')
      .then(response => response.json())
      .then(data => setTasks(data.tasks))
      .catch(error => console.error('Error fetching tasks:', error));

    socket.on('connect', () => {
      console.log('Connected to Socket.io server');  // Log when connected
    });
    
    socket.on('disconnect', () => {
      console.log('Disconnected from Socket.io server');  // Log when disconnected
    });

    socket.on('task_update', (newTask) => {
      setTasks(prevTasks => [...prevTasks, newTask]);
    });

    socket.on('task_deleted', ({ task_id }) => {
      console.log(`Task deleted with ID: ${task_id}`);  // Log for debugging
      setTasks(prevTasks => prevTasks.filter(task => task.id !== task_id));  // Filter out the deleted task
    });
    
    return () => {
      socket.disconnect();
    };
  }, []);

  const completeTask = (task_id) => {
    fetch(`http://127.0.0.1:5000/tasks/${task_id}/complete`, {  
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        console.log('Task completed:', data.message);
        setTasks((prevTasks) => prevTasks.filter((task) => task.id !== task_id));  // Filter out the completed task
      })
      .catch((error) => console.error('Error completing task:', error));
  };
  

  // Function to delete a task
  const deleteTask = (task_id) => {
    fetch(`http://127.0.0.1:5000/api/tasks/${task_id}`, {
      method: 'DELETE',
    })
      .then(response => response.json())
      .then(data => {
        console.log('Task deleted:', data.message);
        setTasks(prevTasks => prevTasks.filter(task => task.id !== task_id));
      })
      .catch(error => console.error('Error deleting task:', error));
  };

  // Handle task click (to reveal complete and delete options)
  const handleTaskClick = (task_id) => {
    setSelectedTask(task_id === selectedTask ? null : task_id);  // Toggle selection
  };

  return (
    <Container>
      <Typography variant="h4" align="center" gutterBottom>
        My To-Do List
      </Typography>

      <Grid container spacing={3}>
        {tasks
          .filter(task => !task.completed)  // Only show tasks that are not completed
          .map((task, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card 
                onClick={() => handleTaskClick(task.id)}  // Select the task when clicked
                sx={{ 
                  backgroundColor: task.completed ? '#e0f7fa' : '#fff3e0',
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