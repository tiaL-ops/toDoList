import React, { useState } from 'react';
import TodoList from './components/ToDoList';
import TodoForm from './components/ToDoForm';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);

  const addTask = (newTask) => {
    setTasks([...tasks, newTask]);
  };

  return (
    <div className="App">
      <h1>Todo Application</h1>
      <TodoForm addTask={addTask} />
      <TodoList />
    </div>
  );
}

export default App;
