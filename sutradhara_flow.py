"""
Sutradhara: The orchestrator and flow controller.
Manages state, routing, schema validation, and retry logic.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from schemas import SurplusReport, ValidatedRecord, RankedMatches, SafetyDecision, FinalDecision
from agents import (
    EklavyaIntakeAgent, ArjunaMatchingAgent, DronacharyyaSafetyAgent, ChanakyaLogisticsAgent
)


class SutradharaFlow:
    """
    Central orchestrator for the CrewAI flow.
    - Creates run ID
    - Passes state through agents
    - Validates schemas at every handoff
    - Retries once on schema failure
    - Records full trace
    """
    
    def __init__(self):
        self.run_log = {}
        self.agents = {
            "eklavya": EklavyaIntakeAgent(),
            "arjuna": ArjunaMatchingAgent(),
            "dronacharya": DronacharyyaSafetyAgent(),
            "chanakya": ChanakyaLogisticsAgent(),
        }
    
    def execute_flow(self, surplus_report: dict) -> Dict[str, Any]:
        """
        Execute the full flow: report → eklavya → arjuna → dronacharya → chanakya → decision.
        """
        
        run_id = str(uuid.uuid4())[:8]
        start_time = datetime.now()
        
        self.run_log[run_id] = {
            "run_id": run_id,
            "start_time": start_time.isoformat(),
            "stages": {},
        }
        
        try:
            # Convert input to SurplusReport
            report = SurplusReport(**surplus_report)
            self._log_stage(run_id, "input", {"report": report.dict()})
            
            # Stage 1: Eklavya Intake & Validation
            validated = self._execute_with_retry(
                run_id,
                "eklavya",
                lambda: self.agents["eklavya"].execute(report),
                ValidatedRecord
            )
            
            if not validated or validated.status == "rejected":
                final = FinalDecision(
                    action="no_pickup",
                    recipient_id=None,
                    recipient_name=None,
                    pickup_time=None,
                    explanation=f"Intake validation failed: {', '.join(validated.issues if validated else [])}",
                    run_id=run_id
                )
                self._log_stage(run_id, "final_decision", final.dict())
                self.run_log[run_id]["end_time"] = datetime.now().isoformat()
                return {"final_decision": final.dict(), "run_id": run_id}
            
            self._log_stage(run_id, "validated_record", validated.dict())
            
            # Stage 2: Arjuna Demand & Matching
            ranked_matches = self._execute_with_retry(
                run_id,
                "arjuna",
                lambda: self.agents["arjuna"].execute(validated),
                RankedMatches
            )
            
            self._log_stage(run_id, "ranked_matches", ranked_matches.dict() if ranked_matches else {})
            
            # Stage 3: Dronacharya Safety & Compliance
            safety_decision = self._execute_with_retry(
                run_id,
                "dronacharya",
                lambda: self.agents["dronacharya"].execute(validated),
                SafetyDecision
            )
            
            self._log_stage(run_id, "safety_decision", safety_decision.dict() if safety_decision else {})
            
            # Stage 4: Chanakya Logistics Manager
            final_decision = self._execute_with_retry(
                run_id,
                "chanakya",
                lambda: self.agents["chanakya"].execute(validated, ranked_matches, safety_decision, run_id),
                FinalDecision
            )
            
            self._log_stage(run_id, "final_decision", final_decision.dict() if final_decision else {})
            
            self.run_log[run_id]["end_time"] = datetime.now().isoformat()
            self.run_log[run_id]["status"] = "completed"
            
            return {
                "final_decision": final_decision.dict() if final_decision else None,
                "run_id": run_id,
                "trace": self.run_log[run_id]
            }
            
        except Exception as e:
            self.run_log[run_id]["status"] = "failed"
            self.run_log[run_id]["error"] = str(e)
            self.run_log[run_id]["end_time"] = datetime.now().isoformat()
            return {
                "error": str(e),
                "run_id": run_id,
                "trace": self.run_log[run_id]
            }
    
    def _execute_with_retry(self, run_id: str, agent_name: str, execute_fn, expected_type):
        """
        Execute agent with one retry on schema failure.
        """
        
        stage_start = datetime.now()
        
        try:
            result = execute_fn()
            
            # Validate schema
            if not isinstance(result, expected_type):
                # Retry once
                result = execute_fn()
                if not isinstance(result, expected_type):
                    raise ValueError(f"{agent_name} produced invalid schema after retry")
            
            stage_end = datetime.now()
            latency_ms = (stage_end - stage_start).total_seconds() * 1000
            
            self.run_log[run_id]["stages"][agent_name] = {
                "status": "success",
                "latency_ms": latency_ms,
                "start_time": stage_start.isoformat(),
                "end_time": stage_end.isoformat(),
            }
            
            return result
            
        except Exception as e:
            stage_end = datetime.now()
            self.run_log[run_id]["stages"][agent_name] = {
                "status": "failed",
                "error": str(e),
                "start_time": stage_start.isoformat(),
                "end_time": stage_end.isoformat(),
            }
            raise
    
    def _log_stage(self, run_id: str, stage_name: str, data: Dict[str, Any]):
        """Log stage output."""
        if run_id not in self.run_log:
            self.run_log[run_id] = {}
        
        self.run_log[run_id][stage_name] = data
    
    def get_run_trace(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve full trace for a run."""
        return self.run_log.get(run_id)
    
    def save_run_to_file(self, run_id: str, filepath: str):
        """Save run trace to JSON file."""
        trace = self.get_run_trace(run_id)
        if trace:
            with open(filepath, 'w') as f:
                json.dump(trace, f, indent=2, default=str)


if __name__ == "__main__":
    # Test the flow
    flow = SutradharaFlow()
    
    test_report = {
        "food_type": "vegetable biryani",
        "quantity": 60,
        "prep_time": "14:00",
        "temperature_c": 58.0,
        "location": "Hostel Mess B",
        "pickup_deadline": "20:00"
    }
    
    result = flow.execute_flow(test_report)
    print("=== Flow Result ===")
    print(json.dumps(result, indent=2, default=str))
