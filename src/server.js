const express = require('express');
const cors = require('cors');
const app = express();

// Enable CORS for all routes and allow requests from localhost:3000
app.use(cors({
  origin: 'http://localhost:3000',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
}));

// Middleware to parse JSON
app.use(express.json());

// Route to handle /test requests
app.get('/test', (req, res) => {
  res.json({ message: 'CORS request successful' });
});

// Handle preflight requests
app.options('*', cors());  // Preflight requests handled automatically for all routes

// Placeholder route for registration or other API endpoints
app.post('/register', (req, res) => {
  // Handle registration logic here
  res.json({ message: 'Registration successful' });
});

// Start the server on port 5000
app.listen(5000, () => {
  console.log('Backend server is running on http://localhost:5000');
});
