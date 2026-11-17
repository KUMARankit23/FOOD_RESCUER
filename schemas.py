"""
Enhanced Data Contracts for Agentic AI
All schemas with LLM reasoning, A2A protocol, and evaluation support
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime


class SurplusReport(BaseModel):
    """Raw surplus food report from a donor."""
    food_type: str = Field(..., description="Type of food")
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
    evidence: List[Evidence] = Field(default_factory=list, description="Cited chunks")


class FinalDecision(BaseModel):
    """Output from Chanakya (Logistics Manager Agent)."""
    action: Literal["dispatch", "hold", "discard", "no_pickup"]
    recipient_id: Optional[str] = None
    recipient_name: Optional[str] = None
    pickup_time: Optional[str] = None
    explanation: str
    run_id: str


class A2AMessage(BaseModel):
    """Agent-to-Agent message"""
    message_id: str
    sender_agent: str
    sender_framework: str
    receiver_agent: str
    receiver_framework: str
    message_type: Literal["request", "response", "state_update"]
    payload: Dict[str, Any]
    timestamp: str


class A2AAgent(BaseModel):
    """Agent registration for discovery"""
    agent_id: str
    agent_name: str
    framework: str
    capabilities: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class BlackboardState(BaseModel):
    """Shared blackboard state for agents"""
    run_id: str
    original_report: Optional[SurplusReport] = None
    validated_record: Optional[ValidatedRecord] = None
    ranked_matches: Optional[RankedMatches] = None
    safety_decision: Optional[SafetyDecision] = None
    final_decision: Optional[FinalDecision] = None
    state_version: int = 0
    agents_notified: List[str] = Field(default_factory=list)


class MCPToolDefinition(BaseModel):
    """MCP Tool schema"""
    tool_name: str
    tool_type: str
    mcp_server: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class MCPToolResult(BaseModel):
    """MCP Tool execution result"""
    tool_name: str
    status: str
    result: Dict[str, Any]
    execution_time_ms: float
    error_message: Optional[str] = None


class A2AMessageType:
    REQUEST = "request"
    RESPONSE = "response"
    STATE_UPDATE = "state_update"
