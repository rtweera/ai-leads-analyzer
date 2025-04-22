from sqlalchemy.orm import Session
from app.db.models.leads_model import AllLeads
from app.schemas.ingress_schema import LeadPayload
from datetime import datetime
from app.crud import constants

def create_lead(db: Session, lead_payload: LeadPayload):
    """
    Create a new lead in the database.
    """
    db_lead = AllLeads(
        event_happened_at=datetime.now(tz=constants.COLOMBO),
        lead_first_name=lead_payload.leadInfo.firstName,
        lead_last_name=lead_payload.leadInfo.lastName,
        lead_email=lead_payload.leadInfo.email,
        lead_phone=lead_payload.leadInfo.phone,
        lead_job_role=lead_payload.leadInfo.jobTitle,
        lead_company=lead_payload.leadInfo.company,
        lead_country=lead_payload.leadInfo.country,
        lead_state=lead_payload.leadInfo.state,
        lead_industry=lead_payload.leadInfo.industry,
        can_help_comment=lead_payload.leadInfo.canHelpComment,
        area_of_interest=lead_payload.leadInfo.areaOfInterest,
        description=lead_payload.leadInfo.contactReason
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead) # Refresh the instance to get the updated state from the database (specially with auto-incremented IDs)
    return db_lead