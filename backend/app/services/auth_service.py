from backend.app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from backend.app.models.user import User
from backend.app.repositories.user_repository import UserRepository
from backend.app.schemas.user import UserCreate


class AuthService:
    """Authentication business logic."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, user_data: UserCreate) -> User:
        existing_user = self.repository.get_by_email(user_data.email)

        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )

        return self.repository.create(user)

    def login(self, email: str, password: str) -> str:
        user = self.repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        return create_access_token(
            data={"sub": user.email}
        )