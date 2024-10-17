# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  
    password_hash = db.Column(db.String(200), nullable=False)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    priority = db.Column(db.String, default='Low')
    category = db.Column(db.String, default='General')
    deadline = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)
    completed_on = db.Column(db.Date)

    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(description={self.description}, priority={self.priority}, category={self.category}, completed={self.completed})>"
