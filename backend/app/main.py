from fastapi import FastAPI
from app.routes import auth

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Hielo Llano"}