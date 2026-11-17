"""
SQLAlchemy ORM Models for Food Rescue MAS
Replaces in-memory storage with persistent database
"""

from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from enum import Enum

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./food_rescue.db")

engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    pool_pre_ping=True if "postgresql" in DATABASE_URL else False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Enum classes
class RunStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DecisionAction(str, Enum):
    DISPATCH = "dispatch"
    HOLD = "hold"
    DISCARD = "discard"
    NO_PICKUP = "no_pickup"


class PickerStatus(str, Enum):
    ASSIGNED = "assigned"
    ACCEPTED = "accepted"
    EN_ROUTE_PICKUP = "en_route_pickup"
    ARRIVED_PICKUP = "arrived_pickup"
    PICKED_UP = "picked_up"
    EN_ROUTE_DELIVERY = "en_route_delivery"
    ARRIVED_DELIVERY = "arrived_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# Database Models

class Donor(Base):
    """Food donor organization"""
    __tablename__ = "donors"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    reports = relationship("FoodReport", back_populates="donor")


class FoodReport(Base):
    """Surplus food donation report"""
    __tablename__ = "food_reports"
    
    id = Column(String, primary_key=True, index=True)
    donor_id = Column(String, ForeignKey("donors.id"))
    food_type = Column(String, index=True)
    quantity = Column(Integer)
    prep_time = Column(String)
    temperature_c = Column(Float)
    location = Column(String)
    pickup_deadline = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    donor = relationship("Donor", back_populates="reports")
    run = relationship("RescueRun", back_populates="report", uselist=False)


class Recipient(Base):
    """Food recipient organization"""
    __tablename__ = "recipients"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    capacity_portions = Column(Integer)
    food_preferences = Column(JSON)  # ["vegetarian", "all", "specific_types"]
    dietary_restrictions = Column(JSON)  # ["halal", "kosher", "vegan"]
    staff_trained = Column(Boolean, default=False)
    contact_email = Column(String)
    contact_phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dispatches = relationship("DispatchRecord", back_populates="recipient")


class RescueRun(Base):
    """Complete rescue workflow run"""
    __tablename__ = "rescue_runs"
    
    id = Column(String, primary_key=True, index=True)
    report_id = Column(String, ForeignKey("food_reports.id"), unique=True)
    status = Column(SQLEnum(RunStatus), default=RunStatus.PENDING, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Trace data
    trace_data = Column(JSON)  # Full execution trace
    
    # Relationships
    report = relationship("FoodReport", back_populates="run")
    agent_executions = relationship("AgentExecution", back_populates="run")
    dispatch = relationship("DispatchRecord", back_populates="run", uselist=False)
    delivery = relationship("DeliveryConfirmation", back_populates="run", uselist=False)


class AgentExecution(Base):
    """Record of agent execution within a run"""
    __tablename__ = "agent_executions"
    
    id = Column(String, primary_key=True, index=True)
    run_id = Column(String, ForeignKey("rescue_runs.id"), index=True)
    agent_name = Column(String, index=True)  # "eklavya", "arjuna", "dronacharya", "chanakya"
    framework = Column(String)  # "adk" or "crewai"
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String)  # "success", "failed"
    latency_ms = Column(Float)
    input_data = Column(JSON)
    output_data = Column(JSON)
    tool_calls = Column(JSON)  # Tools invoked by this agent
    tokens_used = Column(Integer, nullable=True)  # LLM token count
    error_message = Column(Text, nullable=True)
    
    # Relationships
    run = relationship("RescueRun", back_populates="agent_executions")


class AgentMessage(Base):
    """A2A protocol messages between agents"""
    __tablename__ = "agent_messages"
    
    id = Column(String, primary_key=True, index=True)
    run_id = Column(String, ForeignKey("rescue_runs.id"), index=True)
    sender_agent = Column(String)
    sender_framework = Column(String)
    receiver_agent = Column(String)
    receiver_framework = Column(String)
    message_type = Column(String)  # "request", "response", "state_update"
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class SafetyAssessment(Base):
    """Dronacharya's food safety assessment"""
    __tablename__ = "safety_assessments"
    
    id = Column(String, primary_key=True, index=True)
    run_id = Column(String, ForeignKey("rescue_runs.id"), index=True)
    verdict = Column(String)  # "safe", "unsafe", "conditional", "insufficient_evidence"
    reason = Column(Text)
    evidence = Column(JSON)  # Retrieved RAG passages
    source_references = Column(JSON)  # FSSAI citations
    confidence = Column(Float)
    assessed_at = Column(DateTime, default=datetime.utcnow)


class DispatchRecord(Base):
    """Final dispatch decision and assignment"""
    __tablename__ = "dispatch_records"
    
    id = Column(String, primary_key=True, index=True)
    run_id = Column(String, ForeignKey("rescue_runs.id"), unique=True)
    recipient_id = Column(String, ForeignKey("recipients.id"))
    decision_action = Column(SQLEnum(DecisionAction), index=True)
    pickup_time = Column(String, nullable=True)
    assigned_picker_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    run = relationship("RescueRun", back_populates="dispatch")
    recipient = relationship("Recipient", back_populates="dispatches")


class PickerJob(Base):
    """Job assigned to a picker (food delivery agent)"""
    __tablename__ = "picker_jobs"
    
    id = Column(String, primary_key=True, index=True)
    run_id = Column(String, ForeignKey("rescue_runs.id"), unique=True)
    picker_id = Column(String, index=True)
    status = Column(SQLEnum(PickerStatus), default=PickerStatus.ASSIGNED, index=True)
    pickup_location = Column(String)
    pickup_latitude = Column(Float, nullable=True)
    pickup_longitude = Column(Float, nullable=True)
    delivery_location = Column(String)
    delivery_latitude = Column(Float, nullable=True)
    delivery_longitude = Column(Float, nullable=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)


class LocationHistory(Base):
    """GPS location tracking for picker"""
    __tablename__ = "location_history"
    
    id = Column(String, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("picker_jobs.id"), index=True)
    picker_id = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    accuracy_meters = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class DeliveryConfirmation(Base):
    """Recipient confirmation of delivery"""
    __tablename__ = "delivery_confirmations"
    
    id = Column(String, primary_key=True, index=True)
    run_id = Column(String, ForeignKey("rescue_runs.id"), unique=True)
    recipient_id = Column(String, ForeignKey("recipients.id"))
    picker_id = Column(String)
    quantity_received = Column(Integer)
    food_condition = Column(String)  # "good", "acceptable", "poor"
    feedback = Column(Text, nullable=True)
    confirmed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    run = relationship("RescueRun", back_populates="delivery")


class AuditLog(Base):
    """Audit trail for all actions"""
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, index=True)
    run_id = Column(String, ForeignKey("rescue_runs.id"), nullable=True, index=True)
    action = Column(String, index=True)
    actor = Column(String)  # "system", "donor", "picker", "recipient", "admin"
    actor_id = Column(String, nullable=True)
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


# Create tables
def init_db():
    """Initialize all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables initialized")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
