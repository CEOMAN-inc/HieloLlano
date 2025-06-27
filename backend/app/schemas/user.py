from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: int

class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: int