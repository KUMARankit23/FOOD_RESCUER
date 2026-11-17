"""
Google ADK (Agent Development Kit) Integration
Implements the 4 agents using ADK framework pattern
These agents interoperate with CrewAI agents via A2A protocol
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from enhanced_schemas import (
    SurplusReport, ValidatedRecord, RankedMatches, RankedMatch,
    SafetyDecision, FinalDecision, A2AMessageType
)
from a2a_protocol import a2a_protocol


class ADKAgent:
    """Base class for ADK agents"""
    
    def __init__(self, agent_id: str, agent_name: str, framework: str = "adk"):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.framework = framework
        self.state: Dict[str, Any] = {}
        self.execution_log: List[Dict[str, Any]] = []
        self.tools: Dict[str, callable] = {}
    
    def register_tool(self, tool_name: str, tool_func: callable):
        """Register a tool for this agent"""
        self.tools[tool_name] = tool_func
    
    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Execute a registered tool"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not registered")
        
        tool = self.tools[tool_name]
        return tool(**args)
    
    def log_execution(self, event: str, details: Dict[str, Any]):
        """Log agent execution"""
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "event": event,
            "details": details
        })
    
    def think(self, input_data: Any) -> Dict[str, Any]:
        """Reasoning step (ADK pattern)"""
        raise NotImplementedError
    
    def act(self, reasoning: Dict[str, Any]) -> Any:
        """Action step (ADK pattern)"""
        raise NotImplementedError
    
    def execute(self, input_data: Any) -> Any:
        """Full ADK execution: think → act"""
        # Think phase
        reasoning = self.think(input_data)
        self.log_execution("think", reasoning)
        
        # Act phase
        result = self.act(reasoning)
        self.log_execution("act", {"result": str(result)})
        
        return result


class EklavyaADK(ADKAgent):
    """Eklavya Intake Agent using ADK"""
    
    def __init__(self):
        super().__init__("eklavya_adk", "Eklavya (ADK)", "adk")
        self._register_tools()
    
    def _register_tools(self):
        """Register validation tools"""
        self.register_tool("validate_schema", self._validate_schema)
        self.register_tool("check_location", self._check_location)
    
    def _validate_schema(self, report: SurplusReport) -> Dict[str, Any]:
        """Validate report schema"""
        issues = []
        
        if not report.food_type:
            issues.append("Missing food_type")
        if report.quantity <= 0:
            issues.append("Invalid quantity")
        if report.temperature_c < -10 or report.temperature_c > 90:
            issues.append("Invalid temperature")
        if not report.location:
            issues.append("Missing location")
        
        return {"valid": len(issues) == 0, "issues": issues}
    
    def _check_location(self, location: str) -> Dict[str, Any]:
        """Check if location is valid"""
        valid_locations = ["Hostel", "Cafeteria", "Library", "Gym", "Medical"]
        return {
            "valid": location in valid_locations,
            "location": location
        }
    
    def think(self, report: SurplusReport) -> Dict[str, Any]:
        """Reasoning: analyze report structure"""
        return {
            "task": "validate_intake_report",
            "report_type": report.food_type,
            "quantity": report.quantity,
            "checks": ["schema", "location", "time"]
        }
    
    def act(self, reasoning: Dict[str, Any]) -> ValidatedRecord:
        """Action: perform validation"""
        # Simulate getting report from input
        report = SurplusReport(
            food_type="biryani",
            quantity=60,
            prep_time="14:00",
            temperature_c=58.0,
            location="Cafeteria",
            pickup_deadline="20:00"
        )
        
        # Execute validation tools
        schema_result = self.execute_tool("validate_schema", {"report": report})
        location_result = self.execute_tool("check_location", {"location": report.location})
        
        # Combine results
        issues = schema_result.get("issues", [])
        if not location_result.get("valid"):
            issues.append(f"Invalid location: {report.location}")
        
        status = "valid" if not issues else "needs_fix"
        
        return ValidatedRecord(
            report=report,
            status=status,
            issues=issues,
            missing_fields=[]
        )


class ArjunaADK(ADKAgent):
    """Arjuna Matching Agent using ADK"""
    
    def __init__(self):
        super().__init__("arjuna_adk", "Arjuna (ADK)", "adk")
        self._register_tools()
    
    def _register_tools(self):
        """Register matching tools"""
        self.register_tool("query_recipients", self._query_recipients)
        self.register_tool("calculate_distance", self._calculate_distance)
        self.register_tool("score_match", self._score_match)
    
    def _query_recipients(self, food_type: str) -> List[Dict[str, Any]]:
        """Query recipients by food type"""
        recipients = [
            {"id": "r1", "name": "Community Kitchen", "lat": 40.7128, "lon": -74.0060, "capacity": 100},
            {"id": "r2", "name": "Shelter A", "lat": 40.7150, "lon": -74.0050, "capacity": 150},
            {"id": "r3", "name": "Food Bank", "lat": 40.7200, "lon": -74.0100, "capacity": 200}
        ]
        return recipients
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points"""
        # Simplified distance (mock)
        import math
        return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 111  # km
    
    def _score_match(self, recipient: Dict, distance: float) -> float:
        """Score a match"""
        # Score based on distance and capacity
        distance_score = max(0, 100 - distance * 10)
        capacity_score = min(100, recipient.get("capacity", 0) / 2)
        return (distance_score * 0.6 + capacity_score * 0.4)
    
    def think(self, validated_record: ValidatedRecord) -> Dict[str, Any]:
        """Reasoning: identify matching criteria"""
        return {
            "task": "find_recipients",
            "food_type": validated_record.report.food_type,
            "quantity": validated_record.report.quantity,
            "strategy": "rank_by_distance_and_capacity"
        }
    
    def act(self, reasoning: Dict[str, Any]) -> RankedMatches:
        """Action: rank recipients"""
        donor_lat, donor_lon = 40.7100, -74.0060  # Donor location
        
        # Query recipients
        recipients = self.execute_tool("query_recipients", {"food_type": reasoning["food_type"]})
        
        # Score each recipient
        scored_matches = []
        for recipient in recipients:
            distance = self.execute_tool(
                "calculate_distance",
                {"lat1": donor_lat, "lon1": donor_lon, "lat2": recipient["lat"], "lon2": recipient["lon"]}
            )
            score = self.execute_tool("score_match", {"recipient": recipient, "distance": distance})
            
            scored_matches.append({
                "recipient": recipient,
                "distance": distance,
                "score": score
            })
        
        # Sort by score
        scored_matches.sort(key=lambda x: x["score"], reverse=True)
        
        # Create ranked matches
        matches = [
            RankedMatch(
                recipient_id=m["recipient"]["id"],
                recipient_name=m["recipient"]["name"],
                score=m["score"],
                distance_km=m["distance"],
                reason=f"Score: {m['score']:.1f}, Distance: {m['distance']:.1f}km"
            )
            for m in scored_matches[:3]
        ]
        
        return RankedMatches(matches=matches)


class DronacharyyaADK(ADKAgent):
    """Dronacharya Safety Agent using ADK"""
    
    def __init__(self):
        super().__init__("dronacharya_adk", "Dronacharya (ADK)", "adk")
        self._register_tools()
        self.knowledge_base = [
            {"id": "kb_001", "text": "Cooked vegetables must be at 57°C or above"},
            {"id": "kb_002", "text": "Rice should not be kept more than 4 hours at room temp"},
            {"id": "kb_003", "text": "Meat products require 65°C minimum temperature"},
        ]
    
    def _register_tools(self):
        """Register safety tools"""
        self.register_tool("check_temperature", self._check_temperature)
        self.register_tool("retrieve_knowledge", self._retrieve_knowledge)
        self.register_tool("assess_risk", self._assess_risk)
    
    def _check_temperature(self, food_type: str, temperature: float) -> Dict[str, Any]:
        """Check if temperature is safe"""
        safe_temps = {
            "cooked_veg": 57.0,
            "rice": 65.0,
            "meat": 65.0,
            "dairy": 5.0
        }
        min_temp = safe_temps.get(food_type, 57.0)
        return {"safe": temperature >= min_temp, "required": min_temp, "actual": temperature}
    
    def _retrieve_knowledge(self, query: str) -> List[Dict[str, str]]:
        """Retrieve relevant knowledge"""
        # Simple keyword matching
        results = []
        for item in self.knowledge_base:
            if any(word.lower() in item["text"].lower() for word in query.lower().split()):
                results.append(item)
        return results if results else self.knowledge_base[:2]
    
    def _assess_risk(self, temp_check: Dict, retrieval: List) -> str:
        """Assess overall risk"""
        if temp_check["safe"]:
            return "low"
        else:
            return "high"
    
    def think(self, data: Dict) -> Dict[str, Any]:
        """Reasoning: analyze safety requirements"""
        return {
            "task": "assess_food_safety",
            "food_type": data.get("food_type", "cooked_veg"),
            "temperature": data.get("temperature", 60),
            "approach": "evidence_based"
        }
    
    def act(self, reasoning: Dict[str, Any]) -> SafetyDecision:
        """Action: make safety decision with evidence"""
        # Check temperature
        temp_result = self.execute_tool(
            "check_temperature",
            {"food_type": reasoning["food_type"], "temperature": reasoning["temperature"]}
        )
        
        # Retrieve evidence
        evidence_items = self.execute_tool(
            "retrieve_knowledge",
            {"query": reasoning["food_type"]}
        )
        
        # Assess risk
        risk = self.execute_tool("assess_risk", {"temp_check": temp_result, "retrieval": evidence_items})
        
        # Make decision
        verdict = "safe" if temp_result["safe"] else "unsafe"
        reason = f"Temperature {reasoning['temperature']}°C is {'safe' if temp_result['safe'] else 'below minimum'} (required: {temp_result['required']}°C)"
        
        return SafetyDecision(
            verdict=verdict,
            reason=reason,
            evidence=[
                {"chunk_id": e["id"], "text": e["text"]}
                for e in evidence_items
            ]
        )


class ChanakyaADK(ADKAgent):
    """Chanakya Logistics Agent using ADK"""
    
    def __init__(self):
        super().__init__("chanakya_adk", "Chanakya (ADK)", "adk")
        self._register_tools()
    
    def _register_tools(self):
        """Register logistics tools"""
        self.register_tool("schedule_pickup", self._schedule_pickup)
        self.register_tool("check_availability", self._check_availability)
        self.register_tool("generate_decision", self._generate_decision)
    
    def _schedule_pickup(self, recipient_id: str, location: str) -> Dict[str, Any]:
        """Schedule pickup"""
        available_slots = ["17:00", "17:30", "18:00", "18:30", "19:00"]
        return {"recipient_id": recipient_id, "location": location, "available_slots": available_slots}
    
    def _check_availability(self, recipient_id: str) -> bool:
        """Check if recipient is available"""
        available_recipients = ["r1", "r2", "r3"]
        return recipient_id in available_recipients
    
    def _generate_decision(self, checks: Dict) -> str:
        """Generate final decision"""
        if checks.get("validation_ok") and checks.get("safety_ok") and checks.get("match_found"):
            return "dispatch"
        elif not checks.get("validation_ok"):
            return "no_pickup"
        elif not checks.get("safety_ok"):
            return "discard"
        else:
            return "hold"
    
    def think(self, data: Dict) -> Dict[str, Any]:
        """Reasoning: coordinate constraints"""
        return {
            "task": "make_logistics_decision",
            "validation": data.get("validation_ok", False),
            "safety": data.get("safety_ok", False),
            "recipients_available": data.get("matches_available", False),
            "approach": "constraint_satisfaction"
        }
    
    def act(self, reasoning: Dict[str, Any]) -> FinalDecision:
        """Action: make final logistics decision"""
        # Check availability
        available = self.execute_tool("check_availability", {"recipient_id": "r1"})
        
        # Generate decision
        checks = {
            "validation_ok": reasoning["validation"],
            "safety_ok": reasoning["safety"],
            "match_found": reasoning["recipients_available"]
        }
        action = self.execute_tool("generate_decision", {"checks": checks})
        
        # Schedule pickup if applicable
        pickup_time = None
        if action == "dispatch":
            schedule = self.execute_tool("schedule_pickup", {"recipient_id": "r1", "location": "Downtown"})
            pickup_time = schedule["available_slots"][0]
        
        explanation = f"Decision: {action}"
        if action == "dispatch":
            explanation = f"Dispatch to Community Kitchen at {pickup_time}"
        elif action == "discard":
            explanation = "Food safety violation - must discard"
        elif action == "hold":
            explanation = "Holding for next available slot"
        else:
            explanation = "No suitable recipient found"
        
        return FinalDecision(
            action=action,
            recipient_id="r1" if action == "dispatch" else None,
            recipient_name="Community Kitchen" if action == "dispatch" else None,
            pickup_time=pickup_time,
            explanation=explanation,
            run_id="adk_run_001"
        )


class ADKFramework:
    """ADK Framework orchestrator"""
    
    def __init__(self):
        self.agents: Dict[str, ADKAgent] = {}
        self.message_log: List[Dict[str, Any]] = []
    
    def register_agent(self, agent: ADKAgent):
        """Register an agent"""
        self.agents[agent.agent_id] = agent
        print(f"✓ Registered ADK agent: {agent.agent_name}")
    
    def execute_workflow(self, input_report: SurplusReport) -> Dict[str, Any]:
        """Execute sequential ADK workflow"""
        results = {}
        
        print("\n" + "=" * 70)
        print("ADK WORKFLOW EXECUTION")
        print("=" * 70)
        
        # Step 1: Eklavya validates
        print("\n[1] Eklavya (ADK) - Intake & Validation")
        eklavya = self.agents.get("eklavya_adk")
        validated = eklavya.execute(input_report)
        results["validated"] = validated
        print(f"  Status: {validated.status}")
        
        # Step 2: Arjuna ranks recipients
        print("\n[2] Arjuna (ADK) - Matching & Ranking")
        arjuna = self.agents.get("arjuna_adk")
        ranked = arjuna.execute(validated)
        results["ranked"] = ranked
        print(f"  Matches found: {len(ranked.matches)}")
        
        # Step 3: Dronacharya assesses safety
        print("\n[3] Dronacharya (ADK) - Safety & Compliance")
        dronacharya = self.agents.get("dronacharya_adk")
        safety_data = {
            "food_type": input_report.food_type,
            "temperature": input_report.temperature_c
        }
        safety = dronacharya.execute(safety_data)
        results["safety"] = safety
        print(f"  Verdict: {safety.verdict}")
        
        # Step 4: Chanakya makes final decision
        print("\n[4] Chanakya (ADK) - Logistics & Decision")
        chanakya = self.agents.get("chanakya_adk")
        decision_data = {
            "validation_ok": validated.status == "valid",
            "safety_ok": safety.verdict == "safe",
            "matches_available": len(ranked.matches) > 0
        }
        decision = chanakya.execute(decision_data)
        results["decision"] = decision
        print(f"  Action: {decision.action}")
        
        return results
    
    def send_a2a_message(self, from_agent: str, to_agent: str, payload: Dict):
        """Send A2A message to CrewAI agent"""
        message = a2a_protocol.send_request(
            sender_id=from_agent,
            sender_fw="adk",
            receiver_id=to_agent,
            receiver_fw="crewai",
            payload=payload
        )
        self.message_log.append({
            "timestamp": datetime.now().isoformat(),
            "from": from_agent,
            "to": to_agent,
            "message_id": message.message_id
        })
        return message


# Global ADK framework
adk_framework = ADKFramework()


def initialize_adk():
    """Initialize ADK framework with all agents"""
    adk_framework.register_agent(EklavyaADK())
    adk_framework.register_agent(ArjunaADK())
    adk_framework.register_agent(DronacharyyaADK())
    adk_framework.register_agent(ChanakyaADK())


if __name__ == "__main__":
    # Initialize ADK
    initialize_adk()
    
    # Test workflow
    test_report = SurplusReport(
        food_type="cooked_veg",
        quantity=60,
        prep_time="14:00",
        temperature_c=58.0,
        location="Cafeteria",
        pickup_deadline="20:00"
    )
    
    # Execute ADK workflow
    results = adk_framework.execute_workflow(test_report)
    
    print("\n" + "=" * 70)
    print("ADK WORKFLOW RESULTS")
    print("=" * 70)
    print(f"Final Decision: {results['decision'].action}")
    print(f"Explanation: {results['decision'].explanation}")
