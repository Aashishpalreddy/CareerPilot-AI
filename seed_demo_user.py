import sys
import os

# Add the backend path to sys.path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.app.database.session import SessionLocal
from backend.app.repositories.user_repository import UserRepository
from backend.app.services.auth_service import AuthService
from backend.app.schemas.user import UserCreate

def create_demo_user():
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        auth_service = AuthService(user_repo)
        
        email = "demo@careerpilot.ai"
        
        existing = user_repo.get_by_email(email)
        if existing:
            print(f"User {email} already exists!")
            return
            
        user_data = UserCreate(
            full_name="Demo User",
            email=email,
            password="DemoPassword123!"
        )
        
        user = auth_service.register(user_data)
        print(f"Successfully created demo user: {user.email}")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_user()
