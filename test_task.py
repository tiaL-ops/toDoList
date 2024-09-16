import unittest
from todo import add_task, list_tasks, mark_task_complete, delete_task, tasks, Task,save_tasks_to_file
from unittest.mock import mock_open, patch


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        tasks.clear()
    

    def test_add_task(self):
        result = add_task("Buy groceries")
        self.assertEqual(result, 'Task "Buy groceries" added.')
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Buy groceries")
        self.assertFalse(tasks[0].completed)
    

    def test_list_tasks_no_tasks(self):
        result = list_tasks()
        self.assertEqual(result, "No tasks available.")
    
    def test_list_tasks_with_tasks(self):
        add_task("Buy groceries")
        add_task("Walk the dog")
        result = list_tasks()
        expected_result = "1. Buy groceries [✗]\n2. Walk the dog [✗]"
        self.assertEqual(result, expected_result)

    def test_mark_task_complete_valid(self):
        add_task("Buy groceries")
        result = mark_task_complete(1)
        self.assertEqual(result, 'Task "Buy groceries" marked as complete.')
        self.assertTrue(tasks[0].completed)

    def test_mark_task_complete_invalid(self):
        result = mark_task_complete(1)  # No tasks in the list
        self.assertEqual(result, "Invalid task number.")

    def test_delete_task_valid(self):
        add_task("Buy groceries")
        result = delete_task(1)
        self.assertEqual(result, 'Task "Buy groceries" deleted.')
        self.assertEqual(len(tasks), 0)

    def test_delete_task_invalid(self):
        result = delete_task(1)  # No tasks in the list
        self.assertEqual(result, "Invalid task number.")

    def test_complete_task_then_delete(self):
        add_task("Buy groceries")
        mark_task_complete(1)
        result = delete_task(1)
        self.assertEqual(result, 'Task "Buy groceries" deleted.')
        self.assertEqual(len(tasks), 0)

    def test_delete_multiple_tasks(self):
        add_task("Task 1")
        add_task("Task 2")
        add_task("Task 3")
        delete_task(2)  # Delete Task 2
        result = list_tasks()
        expected_result = "1. Task 1 [✗]\n2. Task 3 [✗]"  
        self.assertEqual(result, expected_result)
    
    @patch("builtins.open", new_callable=mock_open)
    def test_add_task_and_save(self, mock_file):
  
        add_task("Buy groceries")

   
        mock_file.assert_called_once_with('tasks.json', 'w')




if __name__ == "__main__":
    unittest.main()
