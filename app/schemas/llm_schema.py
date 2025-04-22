from pydantic import BaseModel, Optional

class ClassificationResponse(BaseModel):
    """
    Response model for classification tasks.
    """
    is_ai: bool
    ai_reason: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "is_ai": True,
                "ai_reason": "Because of this reason"
            }
        }

