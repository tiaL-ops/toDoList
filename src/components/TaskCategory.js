import React from 'react';
import { FormControl, InputLabel, MenuItem, Select } from '@mui/material';

const TaskCategory = ({ category, onCategoryChange }) => {
  const categories = ['Work', 'Personal', 'Urgent']; // Define your categories

  return (
    <FormControl fullWidth>
      <InputLabel>Category</InputLabel>
      <Select
        value={category}
        label="Category"
        onChange={(e) => onCategoryChange(e.target.value)}
      >
        {categories.map((cat) => (
          <MenuItem key={cat} value={cat}>
            {cat}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default TaskCategory;
