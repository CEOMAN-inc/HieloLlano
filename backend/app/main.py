from fastapi import FastAPI
from app.routes import auth
from app.routes import customers

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"]) 

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Hielo Llano"}