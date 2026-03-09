from fastapi import APIRouter, HTTPException
from models.schemas import UserRegister, UserLogin, UserResponse
from database import supabase

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister):
    """Register a new user with email + password."""
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {"name": user.name}
            }
        })
        if not response.user:
            raise HTTPException(status_code=400, detail="Registration failed")
            
        return UserResponse(
            id=response.user.id,
            email=response.user.email,
            name=user.name,
            token=response.session.access_token if response.session else ""
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin):
    """Login with email + password, returns session token."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        if not response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        # Get user metadata
        name = response.user.user_metadata.get("name", "User") if response.user.user_metadata else "User"
        
        return UserResponse(
            id=response.user.id,
            email=response.user.email,
            name=name,
            token=response.session.access_token
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/logout")
async def logout():
    """Invalidate session token (client side discard mostly, or supabase sign out)."""
    try:
        supabase.auth.sign_out()
        return {"status": "success"}
    except Exception:
        return {"status": "success"}
