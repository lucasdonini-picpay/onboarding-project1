from pydantic import BaseModel


class Failure(BaseModel):
    message: str
