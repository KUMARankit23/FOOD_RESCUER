"""
Data contracts for FoodRescue-MAS.
Every arrow in the system is a Pydantic model, frozen before agents are written.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class SurplusReport(BaseModel):
    """Raw surplus food report from a donor."""
    food_type: str = Field(..., description="Type of food (e.g., 'vegetable biryani')")
    quantity: int = Field(..., description="Number of portions")
    prep_time: str = Field(..., description="Time food was prepared (HH:MM)")
    temperature_c: float = Field(..., description="Current holding temperature in Celsius")
    location: str = Field(..., description="Campus location where food is held")
    pickup_deadline: str = Field(..., description="Latest pickup time (HH:MM)")


class ValidatedRecord(BaseModel):
    """Output from Eklavya (Intake & Validation Agent)."""
    report: SurplusReport
    status: Literal["valid", "needs_fix", "rejected"]
    issues: List[str] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)


class RankedMatch(BaseModel):
    """One ranked recipient candidate."""
    recipient_id: str
    recipient_name: str
    score: float = Field(..., description="Matching score 0-100")
    distance_km: float = Field(..., description="Distance to recipient location")
    reason: str = Field(..., description="One-line explanation of ranking")


class RankedMatches(BaseModel):
    """Output from Arjuna (Demand & Matching Agent)."""
    matches: List[RankedMatch] = Field(..., max_items=3)


class Evidence(BaseModel):
    """Evidence chunk cited in a safety decision."""
    chunk_id: str
    text: str


class SafetyDecision(BaseModel):
    """Output from Dronacharya (Safety & Compliance Agent)."""
    verdict: Literal["safe", "unsafe", "conditional"]
    reason: str = Field(..., description="Explanation of the verdict")
    evidence: List[Evidence] = Field(min_items=1, description="At least one cited chunk")


class FinalDecision(BaseModel):
    """Output from Chanakya (Logistics Manager Agent)."""
    action: Literal["dispatch", "hold", "discard", "no_pickup"]
    recipient_id: Optional[str] = None
    recipient_name: Optional[str] = None
    pickup_time: Optional[str] = None
    explanation: str
    run_id: str
