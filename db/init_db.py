from sqlalchemy import create_engine
from models import Base

# Create an SQLite database (tasks.db)
engine = create_engine('sqlite:///tasks.db')

# Create all tables in the database 
Base.metadata.create_all(engine)

print("Database and tables created!")
