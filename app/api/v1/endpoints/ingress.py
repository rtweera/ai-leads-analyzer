from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ingress_schema import LeadPayload
from app.schemas.egress_schema import CreateLeadResponse
from app.crud.crud_lead import create_lead
from app.api.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", tags=["Leads"], response_model=CreateLeadResponse, status_code=201)
async def handle_create_lead(lead_payload: LeadPayload, db: Session = Depends(get_db)):
    """
    Create a new lead.
    """
    _ = create_lead(db, lead_payload)
    return CreateLeadResponse(
        message="Lead created successfully",
        lead=lead_payload
    )