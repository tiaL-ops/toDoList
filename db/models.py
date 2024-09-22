from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Set up base class
Base = declarative_base()

# Define Task model
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    priority = Column(String, default='Low')
    deadline = Column(Date)
    completed = Column(Boolean, default=False)
    completed_on = Column(Date)

    def __repr__(self):
        return f"<Task(description={self.description}, priority={self.priority}, completed={self.completed})>"
