from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Assuming 'db' is your SQLAlchemy instance, initialized in app.py
db = SQLAlchemy()

class Task(db.Model):  # Use db.Model instead of Base
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    priority = db.Column(db.String, default='Low')
    category = db.Column(db.String, default='General')
    deadline = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)
    completed_on = db.Column(db.Date)

    def __repr__(self):
        return f"<Task(description={self.description}, priority={self.priority}, category={self.category}, completed={self.completed})>"
