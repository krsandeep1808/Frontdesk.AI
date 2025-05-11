from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
import os
from . import models
from .db import get_db, Base, engine
from pydantic import BaseModel

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

templates = Jinja2Templates(directory="frontend/templates")

class HelpRequestCreate(BaseModel):
    customer_phone: str
    question: str

class HelpRequestResponse(BaseModel):
    id: int
    customer_phone: str
    question: str
    status: str
    created_at: datetime
    resolved_at: datetime = None
    answer: str = None

class KnowledgeEntryCreate(BaseModel):
    question: str
    answer: str
    source_request_id: int = None

@app.post("/api/help-requests/", response_model=HelpRequestResponse)
def create_help_request(request: HelpRequestCreate, db: Session = Depends(get_db)):
    db_request = models.HelpRequest(
        customer_phone=request.customer_phone,
        question=request.question
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    # Simulate texting the supervisor
    print(f"\n[SUPERVISOR NOTIFICATION] New help request from {request.customer_phone}:")
    print(f"Question: {request.question}")
    print(f"Request ID: {db_request.id}\n")
    
    return db_request

@app.get("/api/help-requests/", response_model=list[HelpRequestResponse])
def get_help_requests(status: str = None, db: Session = Depends(get_db)):
    query = db.query(models.HelpRequest)
    if status:
        query = query.filter(models.HelpRequest.status == status)
    return query.order_by(models.HelpRequest.created_at.desc()).all()

@app.post("/api/help-requests/{request_id}/resolve", response_model=HelpRequestResponse)
def resolve_help_request(
    request_id: int, 
    answer: str, 
    db: Session = Depends(get_db),
    add_to_knowledge: bool = True
):
    db_request = db.query(models.HelpRequest).filter(models.HelpRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Help request not found")
    
    db_request.status = "resolved"
    db_request.answer = answer
    db_request.resolved_at = datetime.now()
    db.commit()
    db.refresh(db_request)
    
    # Simulate texting back the customer
    print(f"\n[CUSTOMER NOTIFICATION] Response to {db_request.customer_phone}:")
    print(f"Your question: {db_request.question}")
    print(f"Our answer: {answer}\n")
    
    # Add to knowledge base if requested
    if add_to_knowledge:
        knowledge_entry = models.KnowledgeEntry(
            question=db_request.question,
            answer=answer,
            source_request_id=request_id
        )
        db.add(knowledge_entry)
        try:
            db.commit()
        except:
            db.rollback()
            # Entry with this question might already exist
    
    return db_request

@app.get("/api/knowledge/", response_model=list[KnowledgeEntryCreate])
def get_knowledge_entries(db: Session = Depends(get_db)):
    return db.query(models.KnowledgeEntry).order_by(models.KnowledgeEntry.created_at.desc()).all()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})