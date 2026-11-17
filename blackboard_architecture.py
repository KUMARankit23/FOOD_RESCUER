"""
Blackboard Architecture Pattern for Multi-Agent Systems
All agents read/write shared state on a central blackboard
"""

import json
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from threading import Lock
from enhanced_schemas import BlackboardState, SurplusReport


class Blackboard:
    """Central blackboard for shared state"""
    
    def __init__(self):
        self.state: Dict[str, BlackboardState] = {}
        self.state_history: Dict[str, List[Dict[str, Any]]] = {}
        self.subscribers: Dict[str, List[Callable]] = {}
        self.lock = Lock()
    
    def create_run(self, run_id: str) -> BlackboardState:
        """Create a new run state"""
        with self.lock:
            if run_id not in self.state:
                self.state[run_id] = BlackboardState(run_id=run_id)
                self.state_history[run_id] = []
        return self.state[run_id]
    
    def update_state(self, run_id: str, agent_id: str, updates: Dict[str, Any]):
        """Update blackboard state (atomic operation)"""
        with self.lock:
            if run_id not in self.state:
                self.create_run(run_id)
            
            current_state = self.state[run_id]
            
            # Update specific fields
            for key, value in updates.items():
                if hasattr(current_state, key):
                    setattr(current_state, key, value)
            
            # Track version and agent
            current_state.state_version += 1
            if agent_id not in current_state.agents_notified:
                current_state.agents_notified.append(agent_id)
            
            # Record history
            self.state_history[run_id].append({
                "version": current_state.state_version,
                "timestamp": datetime.now().isoformat(),
                "agent": agent_id,
                "changes": updates
            })
            
            # Notify subscribers
            self._notify_subscribers(run_id, agent_id, updates)
    
    def get_state(self, run_id: str) -> Optional[BlackboardState]:
        """Get current blackboard state"""
        with self.lock:
            return self.state.get(run_id)
    
    def read_field(self, run_id: str, field_name: str) -> Optional[Any]:
        """Read a specific field from blackboard"""
        with self.lock:
            state = self.state.get(run_id)
            if state and hasattr(state, field_name):
                return getattr(state, field_name)
            return None
    
    def subscribe(self, run_id: str, callback: Callable):
        """Subscribe to state changes"""
        if run_id not in self.subscribers:
            self.subscribers[run_id] = []
        self.subscribers[run_id].append(callback)
    
    def _notify_subscribers(self, run_id: str, agent_id: str, changes: Dict[str, Any]):
        """Notify all subscribers of state change"""
        if run_id in self.subscribers:
            for callback in self.subscribers[run_id]:
                try:
                    callback(run_id, agent_id, changes)
                except Exception as e:
                    print(f"Error notifying subscriber: {e}")
    
    def get_history(self, run_id: str) -> List[Dict[str, Any]]:
        """Get state change history"""
        with self.lock:
            return self.state_history.get(run_id, [])


class BlackboardAgent:
    """Base class for agents using blackboard architecture"""
    
    def __init__(self, agent_id: str, agent_name: str, blackboard: Blackboard):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.blackboard = blackboard
    
    def read_from_blackboard(self, run_id: str, field_name: str) -> Optional[Any]:
        """Read from blackboard"""
        return self.blackboard.read_field(run_id, field_name)
    
    def write_to_blackboard(self, run_id: str, updates: Dict[str, Any]):
        """Write to blackboard"""
        self.blackboard.update_state(run_id, self.agent_id, updates)
    
    def get_full_state(self, run_id: str) -> Optional[BlackboardState]:
        """Get entire blackboard state"""
        return self.blackboard.get_state(run_id)
    
    def execute(self, run_id: str) -> Any:
        """Execute agent logic - to be implemented by subclasses"""
        raise NotImplementedError


class BlackboardEklavya(BlackboardAgent):
    """Eklavya using Blackboard Architecture"""
    
    def execute(self, run_id: str) -> Dict[str, Any]:
        """Validate and write to blackboard"""
        # Read input from blackboard
        report = self.read_from_blackboard(run_id, "original_report")
        
        if not report:
            print(f"✗ No report on blackboard for {run_id}")
            return {"status": "error"}
        
        print(f"[EKLAVYA] Processing: {report.food_type}")
        
        # Validation logic (simplified)
        issues = []
        if report.quantity <= 0:
            issues.append("Invalid quantity")
        if report.temperature_c < -10 or report.temperature_c > 90:
            issues.append("Invalid temperature")
        
        status = "valid" if not issues else "needs_fix"
        
        # Write back to blackboard
        self.write_to_blackboard(run_id, {
            "validated_record": {
                "report": report,
                "status": status,
                "issues": issues,
                "missing_fields": []
            }
        })
        
        return {"status": status, "agent": self.agent_id}


class BlackboardArjuna(BlackboardAgent):
    """Arjuna using Blackboard Architecture"""
    
    def execute(self, run_id: str) -> Dict[str, Any]:
        """Rank recipients and write to blackboard"""
        # Read validated record from blackboard
        validated = self.read_from_blackboard(run_id, "validated_record")
        
        if not validated or validated.get("status") != "valid":
            print(f"✗ Validation failed for {run_id}")
            return {"status": "error"}
        
        report = validated.get("report")
        print(f"[ARJUNA] Ranking recipients for: {report.food_type}")
        
        # Simplified ranking logic
        matches = [
            {
                "recipient_id": "r1",
                "recipient_name": "Community Kitchen",
                "score": 85.0,
                "distance_km": 2.4,
                "reason": "Best match - close and has capacity"
            }
        ]
        
        # Write to blackboard
        self.write_to_blackboard(run_id, {
            "ranked_matches": {"matches": matches}
        })
        
        return {"status": "success", "matches": len(matches), "agent": self.agent_id}


class BlackboardDronacharya(BlackboardAgent):
    """Dronacharya using Blackboard Architecture"""
    
    def execute(self, run_id: str) -> Dict[str, Any]:
        """Assess safety and write to blackboard"""
        # Read data from blackboard
        validated = self.read_from_blackboard(run_id, "validated_record")
        
        if not validated:
            return {"status": "error"}
        
        report = validated.get("report")
        print(f"[DRONACHARYA] Assessing safety for: {report.food_type}")
        
        # Safety check (simplified)
        is_safe = report.temperature_c >= 57.0  # Minimum safe temp
        verdict = "safe" if is_safe else "unsafe"
        
        # Write to blackboard
        self.write_to_blackboard(run_id, {
            "safety_decision": {
                "verdict": verdict,
                "reason": f"Temperature {report.temperature_c}°C is {'above' if is_safe else 'below'} safe minimum",
                "evidence": [{"chunk_id": "kb_001", "text": "Safe temperature guidelines"}]
            }
        })
        
        return {"status": "success", "verdict": verdict, "agent": self.agent_id}


class BlackboardChanakya(BlackboardAgent):
    """Chanakya using Blackboard Architecture"""
    
    def execute(self, run_id: str) -> Dict[str, Any]:
        """Make final decision based on blackboard state"""
        # Read all necessary data from blackboard
        state = self.get_full_state(run_id)
        
        print(f"[CHANAKYA] Making final decision for {run_id}")
        
        # Check all prerequisites
        if not state.validated_record or not state.safety_decision or not state.ranked_matches:
            action = "no_pickup"
            explanation = "Missing required information"
        elif state.safety_decision["verdict"] == "unsafe":
            action = "discard"
            explanation = "Food safety violation"
        elif not state.ranked_matches["matches"]:
            action = "no_pickup"
            explanation = "No compatible recipients"
        else:
            action = "dispatch"
            match = state.ranked_matches["matches"][0]
            explanation = f"Dispatch to {match['recipient_name']}"
        
        # Write final decision to blackboard
        self.write_to_blackboard(run_id, {
            "final_decision": {
                "action": action,
                "recipient_id": None if action != "dispatch" else state.ranked_matches["matches"][0]["recipient_id"],
                "recipient_name": None if action != "dispatch" else state.ranked_matches["matches"][0]["recipient_name"],
                "pickup_time": "18:15" if action == "dispatch" else None,
                "explanation": explanation,
                "run_id": run_id
            }
        })
        
        return {"status": "success", "action": action, "agent": self.agent_id}


class BlackboardOrchestrator:
    """Orchestrates blackboard-based agent execution"""
    
    def __init__(self, blackboard: Blackboard):
        self.blackboard = blackboard
        self.agents: Dict[str, BlackboardAgent] = {}
    
    def register_agent(self, agent: BlackboardAgent):
        """Register an agent"""
        self.agents[agent.agent_id] = agent
    
    def execute_concurrent(self, run_id: str, report: SurplusReport):
        """Execute all agents concurrently (simulated with sequential for demo)"""
        # Initialize blackboard
        self.blackboard.create_run(run_id)
        self.blackboard.update_state(run_id, "system", {
            "original_report": report
        })
        
        results = {}
        agent_order = ["eklavya", "arjuna", "dronacharya", "chanakya"]
        
        # Execute agents in sequence (but all can read/write blackboard)
        for agent_id in agent_order:
            if agent_id in self.agents:
                print(f"\n→ Executing {agent_id}...")
                result = self.agents[agent_id].execute(run_id)
                results[agent_id] = result
        
        # Return final decision
        final_state = self.blackboard.get_state(run_id)
        return {
            "run_id": run_id,
            "final_decision": final_state.final_decision,
            "state_history": self.blackboard.get_history(run_id),
            "results": results
        }


if __name__ == "__main__":
    # Example usage
    blackboard = Blackboard()
    orchestrator = BlackboardOrchestrator(blackboard)
    
    # Register agents
    orchestrator.register_agent(BlackboardEklavya("eklavya", "Eklavya", blackboard))
    orchestrator.register_agent(BlackboardArjuna("arjuna", "Arjuna", blackboard))
    orchestrator.register_agent(BlackboardDronacharya("dronacharya", "Dronacharya", blackboard))
    orchestrator.register_agent(BlackboardChanakya("chanakya", "Chanakya", blackboard))
    
    # Create test report
    report = SurplusReport(
        food_type="biryani",
        quantity=60,
        prep_time="14:00",
        temperature_c=58.0,
        location="Hostel",
        pickup_deadline="20:00"
    )
    
    # Execute
    print("=" * 70)
    print("BLACKBOARD ARCHITECTURE EXECUTION")
    print("=" * 70)
    result = orchestrator.execute_concurrent("run_001", report)
    
    print("\n" + "=" * 70)
    print("FINAL DECISION")
    print("=" * 70)
    print(f"Action: {result['final_decision'].get('action')}")
    print(f"Explanation: {result['final_decision'].get('explanation')}")
