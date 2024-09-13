import unittest
from todo import add_task, list_tasks, tasks  # Import the functions to test

class TestTodoFunctions(unittest.TestCase):

    def setUp(self):
        """This will run before every test to ensure tasks list is cleared"""
        tasks.clear()

    def test_add_task(self):
        # Add a task and check if it was added correctly
        response = add_task("Walk the dog")
        self.assertEqual(response, 'Task "Walk the dog" added.')
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Walk the dog")
        self.assertFalse(tasks[0].completed)

    def test_list_tasks(self):
        # Check that listing tasks works as expected
        add_task("Buy milk")
        add_task("Do homework")
        task_list = list_tasks()
        expected_output = "1. ✗ Buy milk\n2. ✗ Do homework"
        self.assertEqual(task_list, expected_output)


    def test_list_no_tasks(self):
        # Test that listing tasks with no tasks returns the correct message
        task_list = list_tasks()
        self.assertEqual(task_list, "No tasks available.")

if __name__ == '__main__':
    unittest.main()
