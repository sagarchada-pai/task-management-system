import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models import User, Project, Task, TaskStatus, TaskPriority, Comment
from app.core.security import get_password_hash

def init_db():
    # Create all database tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        if db.query(User).first() is not None:
            print("Database already initialized. Skipping...")
            return
        
        # Create test users
        user1 = User(
            email="user1@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User 1",
            is_active=True
        )
        
        user2 = User(
            email="user2@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User 2",
            is_active=True
        )
        
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            is_active=True,
            is_superuser=True
        )
        
        db.add_all([user1, user2, admin])
        db.commit()
        
        # Create projects
        project1 = Project(
            name="Personal Tasks",
            description="My personal tasks and todos",
            owner_id=user1.id
        )
        
        project2 = Project(
            name="Work Projects",
            description="Work-related tasks and projects",
            owner_id=user1.id
        )
        
        project3 = Project(
            name="Team Project",
            description="Collaborative team project",
            owner_id=user2.id
        )
        
        db.add_all([project1, project2, project3])
        db.commit()
        
        # Create tasks
        task1 = Task(
            title="Set up development environment",
            description="Install and configure all necessary tools",
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            due_date=datetime.utcnow() - timedelta(days=1),
            project_id=project1.id,
            owner_id=user1.id
        )
        
        task2 = Task(
            title="Implement user authentication",
            description="Create login and registration endpoints",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            due_date=datetime.utcnow() + timedelta(days=2),
            project_id=project2.id,
            owner_id=user1.id
        )
        
        task3 = Task(
            title="Write API documentation",
            description="Document all API endpoints",
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            due_date=datetime.utcnow() + timedelta(days=5),
            project_id=project3.id,
            owner_id=user2.id
        )
        
        db.add_all([task1, task2, task3])
        db.commit()
        
        # Create comments
        comment1 = Comment(
            content="This task is completed!",
            task_id=task1.id,
            user_id=user1.id
        )
        
        comment2 = Comment(
            content="I'm working on this now",
            task_id=task2.id,
            user_id=user1.id
        )
        
        comment3 = Comment(
            content="Let me know if you need any help",
            task_id=task2.id,
            user_id=user2.id
        )
        
        db.add_all([comment1, comment2, comment3])
        db.commit()
        
        print("Database initialized with test data!")
        print(f"Test user 1: {user1.email} / password123")
        print(f"Test user 2: {user2.email} / password123")
        print(f"Admin user: {admin.email} / admin123")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
