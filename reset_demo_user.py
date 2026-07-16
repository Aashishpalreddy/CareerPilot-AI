import sys
import os
from sqlalchemy import text

# Add the backend path to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.app.database.session import SessionLocal
from backend.app.repositories.user_repository import UserRepository
from backend.app.services.auth_service import AuthService
from backend.app.schemas.user import UserCreate

def reset_auth():
    db = SessionLocal()
    try:
        print("Deleting all existing users...")
        db.execute(text("DELETE FROM users;"))
        db.commit()
        print("All users deleted.")
        
        user_repo = UserRepository(db)
        auth_service = AuthService(user_repo)
        
        email = "demo@careerpilot.ai"
        user_data = UserCreate(
            full_name="Fresh Demo User",
            email=email,
            password="DemoPassword123!"
        )
        
        user = auth_service.register(user_data)
        print(f"Successfully created fresh demo user: {user.email}")
    except Exception as e:
        db.rollback()
        print(f"Error resetting auth: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_auth()
