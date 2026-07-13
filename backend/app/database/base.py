from backend.app.database.session import Base

# Import all models here so Alembic can discover them
from backend.app.models.user import User

__all__ = ["Base", "User"]