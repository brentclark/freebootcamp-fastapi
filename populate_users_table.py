from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy_utils import EmailType, PasswordType
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Define the database connection string
DATABASE_URL = "sqlite:///posts.db"  # Use your SQLite database file name

# Create an SQLite database engine
engine = create_engine(DATABASE_URL, echo=True)  # Set echo to True for debugging

# Declare a base class using Declarative Base
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    password = Column(PasswordType, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("(now())")
    )


# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Query all users from the 'users' table
all_users = session.query(User).all()

# Display the retrieved data
print("Existing Users:")
for user in all_users:
    print(f"ID: {user.id}, Name: {user.email}, Age: {user.password}")

# Insert a new user into the 'users' table
new_user = User(email="brentgclark@gmail.com", password="ABC", created_at=datetime.now())
session.add(new_user)
session.commit()

# Query all users again to include the newly inserted user
all_users = session.query(User).all()

# Display the updated data
print("\nAll Users After Insert:")
for user in all_users:
    print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")

# Close the session
session.close()
