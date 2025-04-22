from app.schemas.ingress_schema import LeadPayload
from pydantic import BaseModel, Field

class CreateLeadResponse(BaseModel):
    message: str = Field(default="Lead created successfully")
    lead: LeadPayload

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Lead created successfully",
                "lead": LeadPayload.Config.json_schema_extra["example"]
            } 
        }
