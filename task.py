#from datetime import datetime
class Task:
    def __init__(self, description,priority="Medium",deadline = None):
        self.description = description
        self.completed = False
        self.priority=priority
        self.deadline = deadline

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"{status} {self.description}"
