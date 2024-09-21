#from datetime import datetime
import uuid
class Task:
    def __init__(self, description,priority="Medium",deadline = None,category="General"):
        self.id = str(uuid.uuid4())
        self.description = description
        
        self.completed = False
        self.priority=priority
        self.deadline = deadline
        self.category = category

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"{status} {self.description}"
