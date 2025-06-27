from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserOut
from app.services.auth import create_user
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter()

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate):
    # Aquí puedes verificar si ya existe el usuario
    result = create_user(user)
    if "error" in result:
        logging.warning(f"Error en el registro de usuario: {result['error']}")
        raise HTTPException(status_code=400, detail=result["error"])
    return result