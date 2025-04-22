from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ingress_schema import LeadPayload
from app.crud.crud_lead import create_lead
from app.api.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", tags=["Leads"])
async def handle_create_lead(lead_payload: LeadPayload, db: Session = Depends(get_db)):
    """
    Create a new lead.
    """
    res = create_lead(db, lead_payload)
    return {"message": "Lead created successfully", "lead": res}