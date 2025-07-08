from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    rol_id: int

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    rol_id: int