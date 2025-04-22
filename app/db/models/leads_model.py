from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, text
from app.db.db import Base

class AllLeads(Base):
    __tablename__ = 'all_leads'

    id = Column(Integer, primary_key=True, index=True)
    record_inserted_at = Column(DateTime, nullable=False, index=True, server_default=text("NOW()"))
    event_happened_at = Column(String, nullable=True)
    lead_first_name = Column(String, nullable=False)
    lead_last_name = Column(String, nullable=False)
    lead_email = Column(String, nullable=False)
    lead_phone = Column(String, nullable=False)
    lead_job_role = Column(String, nullable=False)
    lead_company = Column(String, nullable=False)
    lead_country = Column(String, nullable=False)
    lead_state = Column(String, nullable=True)
    lead_industry = Column(String, nullable=False)
    can_help_comment = Column(String, nullable=False)
    area_of_interest = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_about_ai = Column(Boolean, nullable=True)
    ai_reason = Column(String, nullable=True)
    geranimo_response = Column(JSON, nullable=True)