from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
def test_connection():
    return {"message": "Connection successful!"}
