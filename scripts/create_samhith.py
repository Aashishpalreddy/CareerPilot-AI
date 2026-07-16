import sys
import os
from sqlalchemy.orm import Session

# Add backend directory to sys.path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.database.session import SessionLocal
from backend.app.repositories.user_repository import UserRepository
from backend.app.services.auth_service import AuthService
from backend.app.schemas.user import UserCreate

def create_user():
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        service = AuthService(repo)
        
        user_data = UserCreate(
            full_name="Samhith Reddy",
            email="samhithmuthyala10@gmail.com",
            password="password123"
        )
        
        try:
            service.register(user_data)
            print("User created successfully!")
        except ValueError as e:
            if "already registered" in str(e).lower():
                print("User already exists!")
            else:
                print(f"Error creating user: {e}")
                
    finally:
        db.close()

if __name__ == "__main__":
    create_user()
