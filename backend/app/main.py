from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API cargada correctamente en el servidor"}
