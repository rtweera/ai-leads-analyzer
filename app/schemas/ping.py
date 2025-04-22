from pydantic import BaseModel

class PingResponse(BaseModel):
    message: str = "pong"

    class Config:
        json_schema_extra = {
            "example": {
                "message": "pong"
            }
        }