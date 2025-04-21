from pydantic import BaseModel

class PingResponse(BaseModel):
    message: str = "pong"

    class Config:
        schema_extra = {
            "example": {
                "message": "pong"
            }
        }