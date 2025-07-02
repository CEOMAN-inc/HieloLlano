from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserOut
from app.services.auth import create_user
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.security import create_access_token, get_current_user
from app.services.auth import authenticate_user
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

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token(data={"sub": user["email"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
