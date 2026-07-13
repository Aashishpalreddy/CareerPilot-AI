from fastapi import APIRouter, Depends

from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.schemas.user import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user