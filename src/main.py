from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .controller import cep_controller
import logging

app = FastAPI()
app.include_router(cep_controller.router)


@app.middleware("http")
async def exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logging.error(f"Exception captured by middleware: {e}")
        match e:
            case ValueError():
                return JSONResponse(status_code=400, content={"detail": f"{e}"})
            case _:
                return JSONResponse(
                    status_code=500,
                    content={
                        "detail": "Something went wrong. Please, try again later."
                    },
                )


@app.get("/test")
def test_connection():
    return {"message": "Connection successful!"}
