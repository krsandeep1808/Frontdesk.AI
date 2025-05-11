from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from .db import Base

class HelpRequest(Base):
    __tablename__ = "help_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_phone = Column(String, index=True)
    question = Column(Text)
    status = Column(String, default="pending")  # pending, resolved, unresolved
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    answer = Column(Text, nullable=True)
    
class KnowledgeEntry(Base):
    __tablename__ = "knowledge_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, unique=True, index=True)
    answer = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    source_request_id = Column(Integer, nullable=True)  # ID of the help request that generated this