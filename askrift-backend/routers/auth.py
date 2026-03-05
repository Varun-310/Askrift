from fastapi import APIRouter, HTTPException
from models.schemas import UserRegister, UserLogin, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister):
    """Register a new user with email + password."""
    # TODO: Phase 2 implementation
    pass


@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin):
    """Login with email + password, returns session token."""
    # TODO: Phase 2 implementation
    pass


@router.post("/logout")
async def logout():
    """Invalidate session token."""
    # TODO: Phase 2 implementation
    pass
