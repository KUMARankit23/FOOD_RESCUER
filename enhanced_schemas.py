"""
Enhanced Schemas with A2A Protocol Support and Advanced Patterns
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum


# ============================================================================
# CORE SCHEMAS (Keep existing + enhance)
# ============================================================================

class SurplusReport(BaseModel):
    """Raw surplus food report from a donor."""
    food_type: str = Field(..., description="Type of food")
    quantity: int = Field(..., description="Number of portions")
    prep_time: str = Field(..., description="Time food was prepared")
    temperature_c: float = Field(..., description="Current temperature")
    location: str = Field(..., description="Campus location")
    pickup_deadline: str = Field(..., description="Latest pickup time")


class ValidatedRecord(BaseModel):
    """Output from Eklavya (Intake & Validation)."""
    report: SurplusReport
    status: Literal["valid", "needs_fix", "rejected"]
    issues: List[str] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)


class RankedMatch(BaseModel):
    """One ranked recipient candidate."""
    recipient_id: str
    recipient_name: str
    score: float = Field(..., description="Matching score 0-100")
    distance_km: float = Field(..., description="Distance to recipient")
    reason: str = Field(..., description="Explanation")


class RankedMatches(BaseModel):
    """Output from Arjuna (Demand & Matching)."""
    matches: List[RankedMatch] = Field(..., max_items=3)


class Evidence(BaseModel):
    """Evidence chunk cited in decision."""
    chunk_id: str
    text: str


class SafetyDecision(BaseModel):
    """Output from Dronacharya (Safety & Compliance)."""
    verdict: Literal["safe", "unsafe", "conditional"]
    reason: str
    evidence: List[Evidence] = Field(min_items=1)


class FinalDecision(BaseModel):
    """Output from Chanakya (Logistics Manager)."""
    action: Literal["dispatch", "hold", "discard", "no_pickup"]
    recipient_id: Optional[str] = None
    recipient_name: Optional[str] = None
    pickup_time: Optional[str] = None
    explanation: str
    run_id: str


# ============================================================================
# A2A PROTOCOL SCHEMAS (New)
# ============================================================================

class A2AMessageType(str, Enum):
    """Types of A2A messages"""
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    STATE_UPDATE = "state_update"
    DISCOVERY = "discovery"


class A2AAgent(BaseModel):
    """Agent registry entry for discovery"""
    agent_id: str
    agent_name: str
    framework: Literal["crewai", "adk"]
    capabilities: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class A2AMessage(BaseModel):
    """A2A protocol message for agent communication"""
    message_id: str
    sender_agent: str
    sender_framework: Literal["crewai", "adk"]
    receiver_agent: str
    receiver_framework: Literal["crewai", "adk"]
    message_type: A2AMessageType
    payload: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# BLACKBOARD SCHEMAS (New)
# ============================================================================

class BlackboardState(BaseModel):
    """Shared state on blackboard for all agents"""
    run_id: str
    original_report: Optional[SurplusReport] = None
    validated_record: Optional[ValidatedRecord] = None
    ranked_matches: Optional[RankedMatches] = None
    safety_decision: Optional[SafetyDecision] = None
    final_decision: Optional[FinalDecision] = None
    
    # Shared metadata
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    agents_notified: List[str] = Field(default_factory=list)
    state_version: int = 0


# ============================================================================
# CALLBACK SCHEMAS (New)
# ============================================================================

class CallbackEvent(str, Enum):
    """Types of callback events"""
    AGENT_START = "agent_start"
    AGENT_COMPLETE = "agent_complete"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    TOOL_ERROR = "tool_error"
    DECISION_MADE = "decision_made"
    ERROR = "error"
    STATE_CHANGED = "state_changed"


class CallbackData(BaseModel):
    """Data passed to callback functions"""
    event_type: CallbackEvent
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    agent_id: str
    run_id: str
    data: Dict[str, Any]
    error: Optional[str] = None


# ============================================================================
# GUARDRAILS SCHEMAS (New)
# ============================================================================

class ValidationRule(BaseModel):
    """Rules for input validation"""
    rule_id: str
    rule_type: Literal["injection", "toxic", "type", "range", "format"]
    condition: str
    action: Literal["allow", "block", "warn"]


class GuardrailResult(BaseModel):
    """Result of guardrail validation"""
    passed: bool
    violations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


# ============================================================================
# PROMPT VARIANT SCHEMAS (New)
# ============================================================================

class PromptVariant(str, Enum):
    """Types of prompt variants"""
    REACT = "react"
    FEWSHOT = "fewshot"
    CONSTRAINT = "constraint"
    PERSONA = "persona"
    ZEROSHOTCOT = "zeroshotcot"


class AgentPrompt(BaseModel):
    """Prompt configuration for an agent"""
    agent_id: str
    variant: PromptVariant
    persona: str = "standard"
    temperature: float = Field(0.1, ge=0, le=1)
    max_tokens: int = 2000
    system_prompt: str
    examples: List[Dict[str, str]] = Field(default_factory=list)


# ============================================================================
# PERFORMANCE EVALUATION SCHEMAS (New)
# ============================================================================

class PerformanceMetrics(BaseModel):
    """Performance metrics for a single run"""
    run_id: str
    timestamp: str
    framework: Literal["crewai", "adk"]
    prompt_variant: PromptVariant
    architecture: Literal["sequential", "blackboard", "hierarchical"]
    
    # Timing metrics
    total_latency_ms: float
    per_agent_latency: Dict[str, float]
    
    # Accuracy metrics
    end_to_end_accuracy: float
    per_agent_accuracy: Dict[str, float]
    
    # Cost metrics
    tokens_used: int
    api_calls: int
    estimated_cost: float
    
    # Reliability metrics
    errors: List[str] = Field(default_factory=list)
    retries: int = 0
    success: bool


class ComparativeEvaluation(BaseModel):
    """Comparison across multiple runs with variants"""
    evaluation_id: str
    runs: List[PerformanceMetrics]
    average_latency_ms: float
    average_accuracy: float
    average_cost: float
    best_variant: str
    worst_variant: str
    recommendations: List[str]


# ============================================================================
# AUDIT & OBSERVABILITY SCHEMAS (New)
# ============================================================================

class AuditEntry(BaseModel):
    """Entry in audit trail for compliance"""
    entry_id: str
    timestamp: str
    agent_id: str
    action: str
    details: Dict[str, Any]
    user_id: Optional[str] = None
    status: Literal["success", "failure", "warning"]


class ExecutionTrace(BaseModel):
    """Complete execution trace with provenance"""
    run_id: str
    start_time: str
    end_time: str
    architecture: str
    framework: str
    audit_entries: List[AuditEntry]
    state_transitions: List[Dict[str, Any]]
    decisions_made: List[Dict[str, Any]]


# ============================================================================
# CLOUD DEPLOYMENT SCHEMAS (New)
# ============================================================================

class DeploymentConfig(BaseModel):
    """Configuration for cloud deployment"""
    platform: Literal["aws", "gcp", "azure", "docker"]
    region: str
    instance_type: str
    auto_scale: bool
    monitoring_enabled: bool
    ci_cd_enabled: bool
    api_gateway: Optional[str] = None


class DeploymentStatus(BaseModel):
    """Status of deployed system"""
    deployment_id: str
    platform: str
    status: Literal["running", "stopped", "failed", "scaling"]
    instances_running: int
    health_check_status: bool
    monitoring_dashboard_url: Optional[str] = None


# ============================================================================
# MCP INTEGRATION SCHEMAS (New)
# ============================================================================

class MCPToolDefinition(BaseModel):
    """Definition of an MCP-compliant tool"""
    tool_name: str
    tool_type: Literal["external_api", "database", "file_parser", "calculator"]
    mcp_server: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class MCPToolResult(BaseModel):
    """Result from MCP tool execution"""
    tool_name: str
    status: Literal["success", "error"]
    result: Dict[str, Any]
    execution_time_ms: float
    error_message: Optional[str] = None
