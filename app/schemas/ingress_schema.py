from pydantic import BaseModel, Field, EmailStr, Json
from typing import List, Optional, Any

class EmailInfo(BaseModel):
    subject: str
    from_: Optional[EmailStr] = Field(alias="from")
    to: List[EmailStr]
    cc: List[EmailStr]

    class Config:
        json_schema_extra = {
            "example": {
                "subject": "NEW LEAD from: Bonjour | Alfonso | API Management Contact Us",
                "from": "example@example.com",
                "to": ["johndoe@wso2.com"],
                "cc": ["johndoe@wso2.com", "mail2@example.com", "mail3@example.com"]
            }
        }


class LeadInfo(BaseModel):
    firstName: str
    lastName: str
    email: Optional[EmailStr]
    phone: Optional[str]
    jobTitle: str
    company: str
    country: str
    state: Optional[str]
    areaOfInterest: str
    contactReason: str
    industry: str
    canHelpComment: str

    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe",
                "email": "John@example.com",
                "phone": "+1234567890",
                "jobTitle": "Developer / Engineer",
                "company": "WSO@",
                "country": "Sri Lanka",
                "state": "",
                "areaOfInterest": "API",
                "contactReason": "Other",
                "industry": "IT",
                "canHelpComment": "Test"
            }
        }


class LeadPayload(BaseModel):
    emailInfo: EmailInfo
    leadInfo: LeadInfo
    class Config:
        json_schema_extra = {
            "example": {
                "emailInfo": EmailInfo.Config.json_schema_extra["example"],
                "leadInfo": LeadInfo.Config.json_schema_extra["example"]
            }
        }


class IngressPayload(BaseModel):
    lead: LeadPayload
    geranimo: Json[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "lead": LeadPayload.Config.json_schema_extra["example"],
                "geranimo": "IDK the format yet 🤷‍♀️"
            }
        }