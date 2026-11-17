"""
Test runner: Execute scenarios and evaluate the system.
"""

import json
import time
from sutradhara_flow import SutradharaFlow
from sukshmadarshini_observer import SukshmadarshiniObserver
from vyasa_generator import generate_batch


def main():
    print("=" * 70)
    print("FoodRescue-MAS: Running 40-Scenario Evaluation")
    print("=" * 70)
    
    flow = SutradharaFlow()
    observer = SukshmadarshiniObserver()
    
    # Generate scenarios
    print("\n[1] Generating 40 synthetic scenarios...")
    scenarios = generate_batch(40)
    print(f"    Generated {len(scenarios)} scenarios.")
    
    # Run each scenario through the flow
    print("\n[2] Running scenarios through the flow...")
    successful_runs = 0
    failed_runs = 0
    
    for i, scenario in enumerate(scenarios):
        report = scenario["report"]
        ground_truth = scenario["ground_truth"]
        
        try:
            result = flow.execute_flow(report)
            run_id = result["run_id"]
            trace = result.get("trace", {})
            
            # Record with observer
            observer.record_run(run_id, trace, ground_truth)
            
            # Print progress
            final_decision = result.get("final_decision", {})
            action = final_decision.get("action")
            expected = ground_truth.get("expected_action")
            match = "✓" if action == expected else "✗"
            
            print(f"    [{i+1:2d}] {match} {run_id}: {action} (expected: {expected})")
            
            if action == expected:
                successful_runs += 1
            else:
                failed_runs += 1
                
        except Exception as e:
            print(f"    [{i+1:2d}] ERROR: {str(e)[:50]}")
            failed_runs += 1
    
    # Compute metrics
    print("\n[3] Computing summary metrics...")
    metrics = observer.compute_summary_metrics()
    
    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Total Runs:              {metrics.get('total_runs', 0)}")
    print(f"Successful:              {successful_runs}")
    print(f"Failed:                  {failed_runs}")
    print(f"\nEnd-to-End Accuracy:     {metrics.get('end_to_end_accuracy', 0):.1%}")
    print(f"\nPer-Agent Accuracy:")
    print(f"  - Eklavya (Intake):    {metrics.get('per_agent_accuracy', {}).get('eklavya_intake', 0):.1%}")
    print(f"  - Arjuna (Matching):   {metrics.get('per_agent_accuracy', {}).get('arjuna_matching', 0):.1%}")
    print(f"  - Dronacharya (Safety):{metrics.get('per_agent_accuracy', {}).get('dronacharya_safety', 0):.1%}")
    print(f"\nRetrieval Quality:       {metrics.get('retrieval_quality', 0):.1%}")
    print(f"Average Latency:         {metrics.get('average_latency_ms', 0):.1f} ms")
    print(f"Reliability:             {metrics.get('reliability', 0):.1%}")
    print("=" * 70)
    
    # Save detailed report
    print("\n[4] Saving detailed report to evaluation_report.json...")
    observer.save_detailed_report("evaluation_report.json")
    print("    ✓ Report saved.")
    
    # Definition of done
    accuracy = metrics.get('end_to_end_accuracy', 0)
    print("\n[5] Definition of Done Check:")
    print(f"    • 40 scenarios run:       {'✓' if metrics.get('total_runs') >= 40 else '✗'}")
    print(f"    • ≥75% accuracy:          {'✓' if accuracy >= 0.75 else '✗'} ({accuracy:.1%})")
    print(f"    • All verdicts cited:     {'✓' if metrics.get('retrieval_quality', 0) > 0 else '✗'}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
