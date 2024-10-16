from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = 'tasks'  
    id = db.Column(Integer, primary_key=True)
    description = db.Column(String(255), nullable=False)
    completed = db.Column(Boolean, default=False)
    priority = db.Column(String(50), default='Medium')
    category = db.Column(String(50), default='General')
    deadline = db.Column(DateTime, nullable=True)
    user_id = db.Column(Integer, ForeignKey('user.id'))  
    user = relationship("User", back_populates="tasks")  


class User(db.Model):
    __tablename__ = 'users' 
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(80), unique=True, nullable=False)
    password_hash = db.Column(String(200), nullable=False)
    

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")  # If user is deleted, their tasks are deleted too

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User(username={self.username})>"
