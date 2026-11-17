"""
Sukshmadarshini: The observer and evaluation layer.
Watches every run, records metrics, scores against ground truth.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class SukshmadarshiniObserver:
    """
    Observability and evaluation layer.
    Tracks latency, accuracy, retrieval quality, reliability.
    """
    
    def __init__(self):
        self.runs_data = {}
        self.metrics_summary = {}
    
    def record_run(self, run_id: str, trace: Dict[str, Any], ground_truth: Optional[Dict[str, Any]] = None):
        """Record a complete run with optional ground truth."""
        
        self.runs_data[run_id] = {
            "run_id": run_id,
            "trace": trace,
            "ground_truth": ground_truth,
            "evaluated_at": datetime.now().isoformat(),
        }
        
        if ground_truth:
            self._evaluate_run(run_id)
    
    def _evaluate_run(self, run_id: str):
        """Evaluate a run against ground truth."""
        
        run = self.runs_data[run_id]
        trace = run["trace"]
        ground_truth = run["ground_truth"]
        
        # Extract final decision
        final_decision = trace.get("final_decision", {})
        action = final_decision.get("action")
        expected_action = ground_truth.get("expected_action")
        
        # Accuracy check
        end_to_end_accuracy = 1 if action == expected_action else 0
        
        # Per-agent accuracy
        validated_record = trace.get("validated_record", {})
        validation_accuracy = 1 if validated_record.get("status") == "valid" else 0
        
        ranked_matches = trace.get("ranked_matches", {})
        matches = ranked_matches.get("matches", [])
        compatible_ids = ground_truth.get("compatible_recipients", [])
        matching_accuracy = 1 if matches and matches[0].get("recipient_id") in compatible_ids else 0
        
        safety_decision = trace.get("safety_decision", {})
        safety_verdict = safety_decision.get("verdict")
        is_safe = ground_truth.get("is_safe")
        # For safety: if is_safe=true, verdict should not be "unsafe"
        safety_accuracy = 1 if (is_safe and safety_verdict != "unsafe") or (not is_safe and safety_verdict == "unsafe") else 0
        
        # Retrieval quality (check if evidence chunks are relevant)
        evidence = safety_decision.get("evidence", [])
        retrieval_quality = len(evidence) / 3 if evidence else 0  # Assuming 3 chunks requested
        
        # Latency from stages
        stages = trace.get("stages", {})
        total_latency_ms = sum(s.get("latency_ms", 0) for s in stages.values())
        
        # Reliability: no errors?
        reliability = 1 if trace.get("status") == "completed" else 0
        
        run["evaluation"] = {
            "end_to_end_accuracy": end_to_end_accuracy,
            "per_agent_accuracy": {
                "eklavya": validation_accuracy,
                "arjuna": matching_accuracy,
                "dronacharya": safety_accuracy,
            },
            "retrieval_quality": retrieval_quality,
            "total_latency_ms": total_latency_ms,
            "reliability": reliability,
        }
    
    def compute_summary_metrics(self) -> Dict[str, Any]:
        """Compute aggregate metrics across all runs."""
        
        if not self.runs_data:
            return {}
        
        runs_with_evaluation = [
            r for r in self.runs_data.values()
            if "evaluation" in r
        ]
        
        if not runs_with_evaluation:
            return {}
        
        n = len(runs_with_evaluation)
        
        # Average end-to-end accuracy
        e2e_acc = sum(r["evaluation"]["end_to_end_accuracy"] for r in runs_with_evaluation) / n
        
        # Per-agent accuracy
        eklavya_acc = sum(r["evaluation"]["per_agent_accuracy"]["eklavya"] for r in runs_with_evaluation) / n
        arjuna_acc = sum(r["evaluation"]["per_agent_accuracy"]["arjuna"] for r in runs_with_evaluation) / n
        dronacharya_acc = sum(r["evaluation"]["per_agent_accuracy"]["dronacharya"] for r in runs_with_evaluation) / n
        
        # Average retrieval quality
        retrieval_quality = sum(r["evaluation"]["retrieval_quality"] for r in runs_with_evaluation) / n
        
        # Average latency
        avg_latency_ms = sum(r["evaluation"]["total_latency_ms"] for r in runs_with_evaluation) / n
        
        # Reliability (% of runs completed)
        reliability = sum(r["evaluation"]["reliability"] for r in runs_with_evaluation) / n
        
        self.metrics_summary = {
            "total_runs": n,
            "end_to_end_accuracy": round(e2e_acc, 3),
            "per_agent_accuracy": {
                "eklavya_intake": round(eklavya_acc, 3),
                "arjuna_matching": round(arjuna_acc, 3),
                "dronacharya_safety": round(dronacharya_acc, 3),
            },
            "retrieval_quality": round(retrieval_quality, 3),
            "average_latency_ms": round(avg_latency_ms, 1),
            "reliability": round(reliability, 3),
        }
        
        return self.metrics_summary
    
    def get_run_evaluation(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get evaluation for a specific run."""
        run = self.runs_data.get(run_id)
        if run:
            return run.get("evaluation")
        return None
    
    def save_summary_to_file(self, filepath: str):
        """Save summary metrics to JSON."""
        self.compute_summary_metrics()
        with open(filepath, 'w') as f:
            json.dump({
                "summary": self.metrics_summary,
                "total_runs_recorded": len(self.runs_data),
            }, f, indent=2)
    
    def save_detailed_report(self, filepath: str):
        """Save detailed report for all runs."""
        detailed = {
            "runs": [
                {
                    "run_id": r["run_id"],
                    "evaluation": r.get("evaluation"),
                    "ground_truth": r.get("ground_truth"),
                    "trace": r.get("trace"),
                }
                for r in self.runs_data.values()
            ],
            "summary": self.metrics_summary
        }
        with open(filepath, 'w') as f:
            json.dump(detailed, f, indent=2, default=str)


if __name__ == "__main__":
    # Test observer
    observer = SukshmadarshiniObserver()
    
    # Mock run
    trace = {
        "run_id": "test001",
        "status": "completed",
        "stages": {
            "eklavya": {"latency_ms": 10},
            "arjuna": {"latency_ms": 15},
            "dronacharya": {"latency_ms": 20},
            "chanakya": {"latency_ms": 5},
        },
        "validated_record": {"status": "valid"},
        "ranked_matches": {"matches": [{"recipient_id": "r1"}]},
        "safety_decision": {"verdict": "conditional", "evidence": [{}, {}, {}]},
        "final_decision": {"action": "dispatch"},
    }
    
    ground_truth = {
        "expected_action": "dispatch",
        "compatible_recipients": ["r1", "r2"],
        "is_safe": True,
    }
    
    observer.record_run("test001", trace, ground_truth)
    print("Metrics:", observer.compute_summary_metrics())
