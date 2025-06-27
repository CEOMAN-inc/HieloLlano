from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserOut
from app.services.auth import create_user

router = APIRouter()

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate):
    # Aquí puedes verificar si ya existe el usuario
    return create_user(user)