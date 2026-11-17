"""
Performance Evaluation Framework
Comparative evaluation across:
- Frameworks (CrewAI vs ADK)
- Architectures (Sequential vs Blackboard vs Hierarchical)
- Prompt Variants (ReAct vs Few-shot vs Persona)
Tracks: accuracy, latency, cost, reliability
"""

import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
from enhanced_schemas import PerformanceMetrics, ComparativeEvaluation, PromptVariant
from callback_system import callback_system


class Architecture(str, Enum):
    """System architectures"""
    SEQUENTIAL = "sequential"
    BLACKBOARD = "blackboard"
    HIERARCHICAL = "hierarchical"


class Framework(str, Enum):
    """Agent frameworks"""
    CREWAI = "crewai"
    ADK = "adk"


class EvaluationScenario:
    """Single evaluation scenario"""
    
    def __init__(self, scenario_id: str, framework: Framework, architecture: Architecture, 
                 prompt_variant: PromptVariant):
        self.scenario_id = scenario_id
        self.framework = framework
        self.architecture = architecture
        self.prompt_variant = prompt_variant
        self.execution_count = 0
        self.results: List[PerformanceMetrics] = []
    
    def add_result(self, metrics: PerformanceMetrics):
        """Add execution result"""
        self.results.append(metrics)
        self.execution_count += 1
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics for this scenario"""
        if not self.results:
            return {}
        
        latencies = [r.total_latency_ms for r in self.results]
        accuracies = [r.end_to_end_accuracy for r in self.results]
        costs = [r.estimated_cost for r in self.results]
        
        return {
            "runs": len(self.results),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "min_latency_ms": min(latencies),
            "max_latency_ms": max(latencies),
            "avg_accuracy": sum(accuracies) / len(accuracies),
            "avg_cost": sum(costs) / len(costs),
            "total_errors": sum(len(r.errors) for r in self.results),
            "success_rate": sum(1 for r in self.results if r.success) / len(self.results)
        }


class PerformanceEvaluator:
    """Main evaluator for comparative testing"""
    
    def __init__(self):
        self.scenarios: Dict[str, EvaluationScenario] = {}
        self.evaluations: List[ComparativeEvaluation] = []
        self.test_data: List[Dict[str, Any]] = []
    
    def create_scenario(self, framework: Framework, architecture: Architecture,
                       prompt_variant: PromptVariant) -> EvaluationScenario:
        """Create a new evaluation scenario"""
        scenario_id = f"{framework.value}_{architecture.value}_{prompt_variant.value}"
        
        scenario = EvaluationScenario(scenario_id, framework, architecture, prompt_variant)
        self.scenarios[scenario_id] = scenario
        
        print(f"✓ Created scenario: {scenario_id}")
        return scenario
    
    def run_evaluation(self, scenario_id: str, num_runs: int = 10) -> List[PerformanceMetrics]:
        """Run evaluation for a scenario"""
        if scenario_id not in self.scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        scenario = self.scenarios[scenario_id]
        results = []
        
        print(f"\n→ Running {num_runs} iterations for {scenario_id}...")
        
        for i in range(num_runs):
            start_time = time.time()
            
            # Simulate execution
            metrics = self._simulate_execution(scenario)
            results.append(metrics)
            scenario.add_result(metrics)
            
            elapsed = time.time() - start_time
            status = "✓" if metrics.success else "✗"
            print(f"  {status} Run {i+1}/{num_runs}: {metrics.total_latency_ms:.2f}ms, "
                  f"Accuracy: {metrics.end_to_end_accuracy:.1f}%")
        
        return results
    
    def _simulate_execution(self, scenario: EvaluationScenario) -> PerformanceMetrics:
        """Simulate agent execution"""
        start_time = time.time()
        
        # Simulate latency based on framework/architecture
        if scenario.framework == Framework.CREWAI:
            base_latency = 150
        else:  # ADK
            base_latency = 180
        
        if scenario.architecture == Architecture.SEQUENTIAL:
            arch_factor = 1.0
        elif scenario.architecture == Architecture.BLACKBOARD:
            arch_factor = 1.2  # Slightly slower due to state management
        else:  # HIERARCHICAL
            arch_factor = 1.1
        
        # Prompt variant factor
        if scenario.prompt_variant == PromptVariant.REACT:
            prompt_factor = 1.3  # Slower, more reasoning
        elif scenario.prompt_variant == PromptVariant.FEWSHOT:
            prompt_factor = 1.0
        else:
            prompt_factor = 1.1
        
        total_latency = base_latency * arch_factor * prompt_factor
        
        # Simulate accuracy
        base_accuracy = 0.82
        if scenario.architecture == Architecture.BLACKBOARD:
            base_accuracy += 0.05  # Shared state helps
        if scenario.framework == Framework.CREWAI:
            base_accuracy += 0.03
        
        accuracy = min(100, base_accuracy * 100 + (5 if scenario.prompt_variant == PromptVariant.REACT else 0))
        
        # Cost calculation
        tokens = int(150 + (total_latency - 150) * 2)  # Rough estimate
        api_calls = 4  # 4 agents
        cost = tokens * 0.0001 + api_calls * 0.01
        
        elapsed = time.time() - start_time
        
        # Trigger callbacks
        callback_system.trigger_agent_start("evaluator", scenario.scenario_id, 
                                           framework=scenario.framework.value)
        callback_system.trigger_agent_complete("evaluator", scenario.scenario_id,
                                              accuracy=accuracy, latency=total_latency)
        
        return PerformanceMetrics(
            run_id=f"{scenario.scenario_id}_{scenario.execution_count}",
            timestamp=datetime.now().isoformat(),
            framework=scenario.framework.value,
            prompt_variant=scenario.prompt_variant,
            architecture=scenario.architecture.value,
            total_latency_ms=total_latency,
            per_agent_latency={
                "eklavya": total_latency * 0.25,
                "arjuna": total_latency * 0.25,
                "dronacharya": total_latency * 0.30,
                "chanakya": total_latency * 0.20
            },
            end_to_end_accuracy=accuracy,
            per_agent_accuracy={
                "eklavya": accuracy + 5,
                "arjuna": accuracy + 2,
                "dronacharya": accuracy + 1,
                "chanakya": accuracy - 2
            },
            tokens_used=tokens,
            api_calls=api_calls,
            estimated_cost=cost,
            errors=[],
            retries=0,
            success=True
        )
    
    def run_comparative_evaluation(self, num_runs_per_variant: int = 10) -> ComparativeEvaluation:
        """Run comprehensive comparative evaluation"""
        print("\n" + "=" * 70)
        print("RUNNING COMPARATIVE EVALUATION")
        print("=" * 70)
        
        all_runs = []
        
        # Test all combinations
        frameworks = [Framework.CREWAI, Framework.ADK]
        architectures = [Architecture.SEQUENTIAL, Architecture.BLACKBOARD, Architecture.HIERARCHICAL]
        prompt_variants = [PromptVariant.REACT, PromptVariant.FEWSHOT, PromptVariant.PERSONA]
        
        total_combinations = len(frameworks) * len(architectures) * len(prompt_variants)
        print(f"\nTesting {total_combinations} combinations with {num_runs_per_variant} runs each...")
        print(f"Total executions: {total_combinations * num_runs_per_variant}")
        
        combo_count = 0
        for framework in frameworks:
            for architecture in architectures:
                for variant in prompt_variants:
                    combo_count += 1
                    
                    print(f"\n[{combo_count}/{total_combinations}] {framework.value.upper()} + "
                          f"{architecture.value} + {variant.value}")
                    
                    scenario = self.create_scenario(framework, architecture, variant)
                    results = self.run_evaluation(scenario.scenario_id, num_runs_per_variant)
                    all_runs.extend(results)
        
        # Analyze results
        print("\n" + "=" * 70)
        print("ANALYSIS")
        print("=" * 70)
        
        # Find best and worst
        best_by_accuracy = max(all_runs, key=lambda r: r.end_to_end_accuracy)
        worst_by_accuracy = min(all_runs, key=lambda r: r.end_to_end_accuracy)
        best_by_speed = min(all_runs, key=lambda r: r.total_latency_ms)
        best_by_cost = min(all_runs, key=lambda r: r.estimated_cost)
        
        print(f"\nBest Accuracy: {best_by_accuracy.framework} + {best_by_accuracy.architecture} "
              f"+ {best_by_accuracy.prompt_variant.value}")
        print(f"  Accuracy: {best_by_accuracy.end_to_end_accuracy:.1f}%")
        
        print(f"\nBest Speed: {best_by_speed.framework} + {best_by_speed.architecture} "
              f"+ {best_by_speed.prompt_variant.value}")
        print(f"  Latency: {best_by_speed.total_latency_ms:.2f}ms")
        
        print(f"\nBest Cost: {best_by_cost.framework} + {best_by_cost.architecture} "
              f"+ {best_by_cost.prompt_variant.value}")
        print(f"  Cost: ${best_by_cost.estimated_cost:.4f}")
        
        # Calculate averages
        avg_latency = sum(r.total_latency_ms for r in all_runs) / len(all_runs)
        avg_accuracy = sum(r.end_to_end_accuracy for r in all_runs) / len(all_runs)
        avg_cost = sum(r.estimated_cost for r in all_runs) / len(all_runs)
        
        evaluation = ComparativeEvaluation(
            evaluation_id=f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            runs=all_runs,
            average_latency_ms=avg_latency,
            average_accuracy=avg_accuracy,
            average_cost=avg_cost,
            best_variant=f"{best_by_accuracy.framework}_{best_by_accuracy.architecture}_{best_by_accuracy.prompt_variant.value}",
            worst_variant=f"{worst_by_accuracy.framework}_{worst_by_accuracy.architecture}_{worst_by_accuracy.prompt_variant.value}",
            recommendations=[
                f"Best accuracy ({best_by_accuracy.end_to_end_accuracy:.1f}%): Use {best_by_accuracy.framework} + {best_by_accuracy.architecture}",
                f"Best speed ({best_by_speed.total_latency_ms:.1f}ms): Use {best_by_speed.framework} + {best_by_speed.architecture}",
                f"Best cost (${best_by_cost.estimated_cost:.4f}): Use {best_by_cost.framework} + {best_by_cost.architecture}",
                "Consider BlackBoard architecture for improved accuracy (State sharing helps decisions)"
            ]
        )
        
        self.evaluations.append(evaluation)
        return evaluation
    
    def generate_report(self, evaluation: ComparativeEvaluation) -> str:
        """Generate evaluation report"""
        report = f"""
PERFORMANCE EVALUATION REPORT
{'=' * 70}
Evaluation ID: {evaluation.evaluation_id}
Total Runs: {len(evaluation.runs)}
Timestamp: {datetime.now().isoformat()}

SUMMARY STATISTICS
{'-' * 70}
Average Latency: {evaluation.average_latency_ms:.2f}ms
Average Accuracy: {evaluation.average_accuracy:.1f}%
Average Cost: ${evaluation.average_cost:.4f}

BEST PERFORMERS
{'-' * 70}
Best Variant (Accuracy): {evaluation.best_variant}
Worst Variant: {evaluation.worst_variant}

RECOMMENDATIONS
{'-' * 70}
"""
        for i, rec in enumerate(evaluation.recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += f"\n{'=' * 70}\n"
        return report
    
    def export_results(self, filepath: str, evaluation: ComparativeEvaluation):
        """Export results to JSON"""
        data = {
            "evaluation_id": evaluation.evaluation_id,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_runs": len(evaluation.runs),
                "average_latency_ms": evaluation.average_latency_ms,
                "average_accuracy": evaluation.average_accuracy,
                "average_cost": evaluation.average_cost
            },
            "runs": [
                {
                    "run_id": r.run_id,
                    "framework": r.framework,
                    "architecture": r.architecture,
                    "prompt_variant": r.prompt_variant.value,
                    "latency_ms": r.total_latency_ms,
                    "accuracy": r.end_to_end_accuracy,
                    "cost": r.estimated_cost,
                    "success": r.success
                }
                for r in evaluation.runs
            ],
            "recommendations": evaluation.recommendations
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Results exported to {filepath}")


# Global evaluator
evaluator = PerformanceEvaluator()


if __name__ == "__main__":
    print("=" * 70)
    print("PERFORMANCE EVALUATOR DEMO")
    print("=" * 70)
    
    # Run comparative evaluation (reduced for demo)
    print("\nRunning comparative evaluation (3 runs per variant for demo)...")
    evaluation = evaluator.run_comparative_evaluation(num_runs_per_variant=3)
    
    # Generate report
    report = evaluator.generate_report(evaluation)
    print(report)
    
    # Export results
    evaluator.export_results("performance_results.json", evaluation)
    
    print("✓ Performance evaluation complete")
