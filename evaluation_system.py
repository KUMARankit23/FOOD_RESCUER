"""
Advanced Agent Evaluation and Observability System
Benchmarks agents, compares architectures, measures performance
"""

import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class EvaluationMetric(str, Enum):
    """Evaluation metrics"""
    ACCURACY = "accuracy"
    LATENCY = "latency_ms"
    PRECISION = "precision"
    RECALL = "recall"
    F1 = "f1"
    CONFIDENCE = "confidence"
    TOKEN_USAGE = "token_usage"
    RAG_PRECISION = "rag_precision"
    RAG_RECALL = "rag_recall"


@dataclass
class AgentMetrics:
    """Metrics for a single agent"""
    agent_name: str
    framework: str  # "adk" or "crewai"
    execution_count: int = 0
    total_latency_ms: float = 0.0
    success_count: int = 0
    error_count: int = 0
    avg_confidence: float = 0.0
    total_tokens: int = 0


@dataclass
class RunEvaluation:
    """Evaluation of a single run"""
    run_id: str
    food_type: str
    expected_action: str
    actual_action: str
    is_correct: bool
    confidence: float
    total_latency_ms: float
    agent_latencies: Dict[str, float]
    rag_precision_at_3: float
    llm_tokens: int
    timestamp: str


class EvaluationSystem:
    """Central evaluation and monitoring system"""
    
    def __init__(self):
        self.runs: Dict[str, RunEvaluation] = {}
        self.agent_metrics: Dict[str, AgentMetrics] = {
            "eklavya": AgentMetrics("eklavya", "adk"),
            "arjuna": AgentMetrics("arjuna", "adk"),
            "dronacharya": AgentMetrics("dronacharya", "adk"),
            "chanakya": AgentMetrics("chanakya", "adk")
        }
        self.architecture_comparison: Dict[str, Any] = {}
    
    def record_run(
        self,
        run_id: str,
        food_type: str,
        expected_action: str,
        actual_action: str,
        confidence: float,
        total_latency_ms: float,
        agent_latencies: Dict[str, float],
        rag_precision: float,
        llm_tokens: int
    ):
        """Record a single run evaluation"""
        
        is_correct = expected_action == actual_action
        
        evaluation = RunEvaluation(
            run_id=run_id,
            food_type=food_type,
            expected_action=expected_action,
            actual_action=actual_action,
            is_correct=is_correct,
            confidence=confidence,
            total_latency_ms=total_latency_ms,
            agent_latencies=agent_latencies,
            rag_precision_at_3=rag_precision,
            llm_tokens=llm_tokens,
            timestamp=datetime.now().isoformat()
        )
        
        self.runs[run_id] = evaluation
        
        # Update agent metrics
        for agent_name, latency in agent_latencies.items():
            if agent_name in self.agent_metrics:
                metrics = self.agent_metrics[agent_name]
                metrics.execution_count += 1
                metrics.total_latency_ms += latency
                if is_correct:
                    metrics.success_count += 1
                else:
                    metrics.error_count += 1
                metrics.avg_confidence = (
                    (metrics.avg_confidence * (metrics.execution_count - 1) + confidence) /
                    metrics.execution_count
                )
                metrics.total_tokens += llm_tokens
    
    def get_summary_metrics(self) -> Dict[str, Any]:
        """Get overall summary metrics"""
        
        if not self.runs:
            return {}
        
        all_runs = list(self.runs.values())
        
        # Overall accuracy
        correct_count = sum(1 for r in all_runs if r.is_correct)
        overall_accuracy = correct_count / len(all_runs) if all_runs else 0
        
        # Average latency per agent
        agent_avg_latency = {}
        for agent_name, metrics in self.agent_metrics.items():
            if metrics.execution_count > 0:
                agent_avg_latency[agent_name] = metrics.total_latency_ms / metrics.execution_count
        
        # RAG evaluation
        avg_rag_precision = sum(r.rag_precision_at_3 for r in all_runs) / len(all_runs) if all_runs else 0
        
        # Total tokens
        total_tokens = sum(r.llm_tokens for r in all_runs)
        
        # Per-food-type accuracy
        food_accuracy = {}
        for food_type in set(r.food_type for r in all_runs):
            food_runs = [r for r in all_runs if r.food_type == food_type]
            food_correct = sum(1 for r in food_runs if r.is_correct)
            food_accuracy[food_type] = food_correct / len(food_runs) if food_runs else 0
        
        return {
            "total_runs": len(all_runs),
            "overall_accuracy": round(overall_accuracy, 3),
            "correct_decisions": correct_count,
            "avg_latency_ms": round(sum(r.total_latency_ms for r in all_runs) / len(all_runs), 2),
            "agent_average_latency": {k: round(v, 2) for k, v in agent_avg_latency.items()},
            "rag_precision_at_3": round(avg_rag_precision, 3),
            "total_llm_tokens": total_tokens,
            "per_food_type_accuracy": {k: round(v, 3) for k, v in food_accuracy.items()},
            "agent_metrics": {
                name: asdict(metrics) for name, metrics in self.agent_metrics.items()
            }
        }
    
    def compare_architectures(
        self,
        architecture_name: str,
        accuracy: float,
        avg_latency: float,
        token_usage: int
    ):
        """Record architecture comparison"""
        self.architecture_comparison[architecture_name] = {
            "accuracy": accuracy,
            "latency_ms": avg_latency,
            "token_usage": token_usage,
            "recorded_at": datetime.now().isoformat()
        }
    
    def get_architecture_comparison(self) -> Dict[str, Any]:
        """Get architecture comparison results"""
        return self.architecture_comparison
    
    def export_report(self, filepath: str = "evaluation_report.json"):
        """Export evaluation report to file"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.get_summary_metrics(),
            "architecture_comparison": self.get_architecture_comparison(),
            "detailed_runs": [asdict(r) for r in self.runs.values()]
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath


class BenchmarkScenarioGenerator:
    """Generates benchmark scenarios for evaluation"""
    
    def __init__(self):
        self.scenarios = self._generate_scenarios()
    
    def _generate_scenarios(self) -> List[Dict[str, Any]]:
        """Generate diverse test scenarios"""
        scenarios = [
            # Normal case - safe food
            {
                "name": "valid_biryani",
                "report": {
                    "food_type": "vegetable biryani",
                    "quantity": 60,
                    "prep_time": "14:00",
                    "temperature_c": 58.0,
                    "location": "Hostel Mess A",
                    "pickup_deadline": "20:00"
                },
                "expected_action": "dispatch"
            },
            # Temperature-critical
            {
                "name": "unsafe_temperature",
                "report": {
                    "food_type": "chicken curry",
                    "quantity": 40,
                    "prep_time": "14:00",
                    "temperature_c": 35.0,
                    "location": "Canteen",
                    "pickup_deadline": "20:00"
                },
                "expected_action": "discard"
            },
            # Cooked rice (high risk)
            {
                "name": "cooked_rice",
                "report": {
                    "food_type": "cooked rice",
                    "quantity": 80,
                    "prep_time": "14:00",
                    "temperature_c": 60.0,
                    "location": "Hostel Mess B",
                    "pickup_deadline": "18:00"
                },
                "expected_action": "dispatch"
            },
            # Dairy product
            {
                "name": "dairy_safe",
                "report": {
                    "food_type": "paneer curry",
                    "quantity": 30,
                    "prep_time": "13:30",
                    "temperature_c": 5.0,
                    "location": "Cafeteria",
                    "pickup_deadline": "17:00"
                },
                "expected_action": "dispatch"
            },
            # Uncertain case
            {
                "name": "uncertain_condition",
                "report": {
                    "food_type": "mixed vegetables",
                    "quantity": 50,
                    "prep_time": "15:00",
                    "temperature_c": 45.0,
                    "location": "Canteen",
                    "pickup_deadline": "19:00"
                },
                "expected_action": "conditional"
            },
            # Missing information
            {
                "name": "incomplete_report",
                "report": {
                    "food_type": "unknown food",
                    "quantity": 0,
                    "prep_time": "unknown",
                    "temperature_c": -10.0,
                    "location": "Unknown",
                    "pickup_deadline": "23:59"
                },
                "expected_action": "no_pickup"
            }
        ]
        
        return scenarios
    
    def get_scenarios(self) -> List[Dict[str, Any]]:
        """Get all scenarios"""
        return self.scenarios
    
    def get_scenario(self, name: str) -> Optional[Dict[str, Any]]:
        """Get specific scenario by name"""
        return next((s for s in self.scenarios if s["name"] == name), None)


class PerformanceMonitor:
    """Monitor system performance and latency"""
    
    def __init__(self):
        self.timings: Dict[str, List[float]] = {}
    
    def record_latency(self, operation: str, latency_ms: float):
        """Record operation latency"""
        if operation not in self.timings:
            self.timings[operation] = []
        self.timings[operation].append(latency_ms)
    
    def get_stats(self, operation: str) -> Dict[str, float]:
        """Get latency statistics for an operation"""
        if operation not in self.timings or not self.timings[operation]:
            return {}
        
        times = sorted(self.timings[operation])
        n = len(times)
        
        return {
            "count": n,
            "min_ms": min(times),
            "max_ms": max(times),
            "avg_ms": sum(times) / n,
            "median_ms": times[n // 2],
            "p95_ms": times[int(n * 0.95)] if n > 1 else times[0],
            "p99_ms": times[int(n * 0.99)] if n > 1 else times[0]
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all operations"""
        return {op: self.get_stats(op) for op in self.timings.keys()}


# Global evaluation system
evaluation_system = EvaluationSystem()
benchmark_generator = BenchmarkScenarioGenerator()
performance_monitor = PerformanceMonitor()


def get_evaluation_system() -> EvaluationSystem:
    """Get global evaluation system"""
    return evaluation_system


def get_benchmark_generator() -> BenchmarkScenarioGenerator:
    """Get benchmark scenario generator"""
    return benchmark_generator


def get_performance_monitor() -> PerformanceMonitor:
    """Get performance monitor"""
    return performance_monitor
