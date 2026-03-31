from fastapi import FastAPI
from .controller import cep_controller

app = FastAPI()
app.include_router(cep_controller.router)


@app.get("/test")
def test_connection():
    return {"message": "Connection successful!"}
