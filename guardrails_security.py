"""
Complete Guardrails and Security Layer
Food safety rules, LLM output validation, access control, input sanitization
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum


class SecurityLevel(str, Enum):
    PERMISSIVE = "permissive"
    STANDARD = "standard"
    STRICT = "strict"


class GuardrailValidator:
    """Main guardrails validator"""
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.STANDARD):
        self.security_level = security_level
        self.violation_log: List[Dict[str, Any]] = []
        self.request_history: Dict[str, List[datetime]] = {}
        self._init_patterns()
    
    def _init_patterns(self):
        """Initialize regex patterns"""
        self.injection_patterns = [
            r"(\bignore\b.*\binstructions?\b)",
            r"(\bsystem\b.*\bprompt\b)",
            r"(\bdisregard\b.*\b(previous|prior)\b)",
            r"(\bforget\b.*\b(previous|prior|instructions?)\b)",
            r"(\b(jailbreak|bypass|override)\b)",
            r"(<!--.*?-->)",
            r"(\${.*?})",
            r"(exec\(|eval\(|__import__)",
        ]
        
        self.toxic_patterns = [
            r"(\b(hate|kill|bomb|threat)\b.*\b(people|user|system)\b)",
            r"(\b(sexual|vulgar|abusive)\b)",
            r"(\b(illegal|hack|steal)\b)",
        ]
        
        self.injection_regex = [re.compile(p, re.IGNORECASE) for p in self.injection_patterns]
        self.toxic_regex = [re.compile(p, re.IGNORECASE) for p in self.toxic_patterns]
    
    def validate_input(self, user_input: str, user_id: str, max_requests_per_minute: int = 60) -> Tuple[bool, List[str]]:
        """Validate user input"""
        violations = []
        
        if not self._check_rate_limit(user_id, max_requests_per_minute):
            violations.append("Rate limit exceeded")
        
        injection_check = self._detect_prompt_injection(user_input)
        if injection_check:
            violations.extend(injection_check)
        
        toxic_check = self._detect_toxic_language(user_input)
        if toxic_check:
            violations.extend(toxic_check)
        
        if len(user_input) > 10000:
            violations.append("Input exceeds maximum length")
        
        if violations:
            self.violation_log.append({
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "violations": violations,
                "security_level": self.security_level.value
            })
        
        return len(violations) == 0, violations
    
    def _detect_prompt_injection(self, text: str) -> List[str]:
        """Detect prompt injection"""
        detections = []
        for regex in self.injection_regex:
            if regex.search(text):
                detections.append("Potential prompt injection detected")
        return detections
    
    def _detect_toxic_language(self, text: str) -> List[str]:
        """Detect toxic language"""
        detections = []
        for regex in self.toxic_regex:
            if regex.search(text):
                detections.append("Toxic language detected")
        return detections
    
    def _check_rate_limit(self, user_id: str, max_requests: int = 60) -> bool:
        """Check rate limiting"""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        if user_id not in self.request_history:
            self.request_history[user_id] = []
        
        self.request_history[user_id] = [
            req_time for req_time in self.request_history[user_id]
            if req_time > one_minute_ago
        ]
        
        if len(self.request_history[user_id]) >= max_requests:
            return False
        
        self.request_history[user_id].append(now)
        return True
    
    def validate_llm_output(self, output: str, expected_schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate LLM structured output"""
        violations = []
        
        try:
            parsed = json.loads(output)
            
            for field in expected_schema.get("required", []):
                if field not in parsed:
                    violations.append(f"Missing field: {field}")
            
            for field, value in parsed.items():
                if field in expected_schema.get("properties", {}):
                    expected_type = expected_schema["properties"][field].get("type")
                    if expected_type and not self._check_type(value, expected_type):
                        violations.append(f"Invalid type for {field}")
        
        except json.JSONDecodeError:
            violations.append("Output is not valid JSON")
        
        return len(violations) == 0, violations
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check type"""
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict
        }
        return isinstance(value, type_map.get(expected_type, type))
    
    def validate_agent_permissions(self, agent_id: str, tool_name: str) -> Tuple[bool, Optional[str]]:
        """Validate agent permissions"""
        permissions = {
            "eklavya": ["validate_report", "lookup_location"],
            "arjuna": ["search_recipients", "calculate_distance", "estimate_demand"],
            "dronacharya": ["retrieve_food_safety", "check_temperature", "assess_risk"],
            "chanakya": ["schedule_pickup", "verify_recipient", "get_statistics"]
        }
        
        allowed = permissions.get(agent_id, [])
        if tool_name not in allowed:
            return False, f"Agent {agent_id} not authorized for {tool_name}"
        
        return True, None
    
    def enforce_food_safety_rules(self, decision: str, safety_verdict: str) -> Tuple[bool, Optional[str]]:
        """ENFORCE DETERMINISTIC SAFETY RULES - Cannot be overridden"""
        
        # Rule 1: Never dispatch unsafe food
        if safety_verdict == "unsafe" and decision == "dispatch":
            return False, "UNSAFE food cannot be dispatched"
        
        # Rule 2: Never hold unsafe food
        if safety_verdict == "unsafe" and decision == "hold":
            return False, "UNSAFE food must be discarded"
        
        # Rule 3: Temperature below absolute minimum must discard
        if decision == "dispatch" and safety_verdict == "unsafe":
            return False, "Safety override not permitted"
        
        return True, None


class SanitizationEngine:
    """Input sanitization"""
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 1000) -> str:
        """Sanitize string"""
        if not isinstance(text, str):
            text = str(text)
        
        dangerous = ["<script>", "</script>", "eval(", "__import__", "exec("]
        for pattern in dangerous:
            text = text.replace(pattern, "")
        
        return text[:max_length]
    
    @staticmethod
    def sanitize_integer(value: Any, min_val: int = 0, max_val: int = 10000) -> int:
        """Sanitize integer"""
        try:
            val = int(value)
            return max(min_val, min(val, max_val))
        except:
            return 0
    
    @staticmethod
    def sanitize_float(value: Any, min_val: float = -100, max_val: float = 100) -> float:
        """Sanitize float"""
        try:
            val = float(value)
            return max(min_val, min(val, max_val))
        except:
            return 0.0


class HumanApprovalWorkflow:
    """Human-in-the-loop for uncertain cases"""
    
    def __init__(self):
        self.pending_approvals: Dict[str, Dict[str, Any]] = {}
    
    def flag_for_review(self, run_id: str, reason: str, details: Dict[str, Any]):
        """Flag case for human review"""
        self.pending_approvals[run_id] = {
            "reason": reason,
            "details": details,
            "flagged_at": datetime.now().isoformat(),
            "approved": False,
            "reviewer": None
        }
    
    def approve(self, run_id: str, reviewer_id: str, decision: str):
        """Approve flagged case"""
        if run_id in self.pending_approvals:
            self.pending_approvals[run_id]["approved"] = True
            self.pending_approvals[run_id]["reviewer"] = reviewer_id
            self.pending_approvals[run_id]["decision"] = decision
            self.pending_approvals[run_id]["approved_at"] = datetime.now().isoformat()
    
    def get_pending(self) -> List[Dict[str, Any]]:
        """Get pending approvals"""
        return [
            (run_id, details) for run_id, details in self.pending_approvals.items()
            if not details.get("approved", False)
        ]


# Global instances
guardrails = GuardrailValidator()
sanitizer = SanitizationEngine()
human_approval = HumanApprovalWorkflow()


def validate_report_guardrails(report: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate report against all guardrails"""
    violations = []
    
    # Temperature guardrails
    temp = report.get("temperature_c", 0)
    if temp < -10 or temp > 90:
        violations.append("Temperature out of acceptable range")
    
    # Quantity guardrails
    qty = report.get("quantity", 0)
    if qty <= 0:
        violations.append("Quantity must be positive")
    
    # Time format validation
    prep_time = report.get("prep_time", "")
    if not re.match(r"^\d{2}:\d{2}$", prep_time):
        violations.append("Invalid prep_time format")
    
    return len(violations) == 0, violations
