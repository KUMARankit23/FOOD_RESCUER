#!/usr/bin/env python
"""
FoodRescue-MAS Main Entry Point.
Choose how you want to interact with the system.
"""

import sys
import subprocess
import time
from pathlib import Path


def main():
    print("\n" + "=" * 70)
    print("🍛 FoodRescue-MAS: Multi-Agent System for Food Redistribution")
    print("=" * 70)
    print("\nChoose how you'd like to interact with the system:\n")
    print("1. Run Full Evaluation (40 scenarios, metrics, report)")
    print("2. Start REST API Server (localhost:8000)")
    print("3. Start Streamlit Dashboard (localhost:8501)")
    print("4. Test Single Report (interactive)")
    print("5. View Help & Documentation")
    print("6. Exit")
    print("\n" + "-" * 70)
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        print("\n📊 Running 40-Scenario Evaluation...")
        print("This will take 2-5 minutes.\n")
        subprocess.run([sys.executable, "test_runner.py"])
        
    elif choice == "2":
        print("\n🚀 Starting REST API Server...")
        print("   API will be available at: http://localhost:8000")
        print("   API Docs at: http://localhost:8000/docs")
        print("   Press Ctrl+C to stop.\n")
        subprocess.run([sys.executable, "-m", "uvicorn", "api:app", "--reload"])
        
    elif choice == "3":
        print("\n📈 Starting Streamlit Dashboard...")
        print("   Dashboard will open at: http://localhost:8501")
        print("   Press Ctrl+C to stop.\n")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_dashboard.py"])
        
    elif choice == "4":
        print("\n📋 Testing Single Report (Interactive)\n")
        test_single_report()
        
    elif choice == "5":
        print_help()
        
    elif choice == "6":
        print("\nGoodbye! 👋\n")
        sys.exit(0)
        
    else:
        print("Invalid choice. Please enter 1-6.")
        main()


def test_single_report():
    """Interactive test of a single report."""
    from sutradhara_flow import SutradharaFlow
    import json
    
    print("Enter report details (or press Enter for defaults):\n")
    
    food_type = input("Food Type (default: vegetable biryani): ").strip() or "vegetable biryani"
    quantity = input("Quantity portions (default: 60): ").strip()
    quantity = int(quantity) if quantity else 60
    prep_time = input("Prep Time HH:MM (default: 14:00): ").strip() or "14:00"
    temp = input("Temperature °C (default: 58): ").strip()
    temperature_c = float(temp) if temp else 58.0
    location = input("Location (default: Hostel Mess B): ").strip() or "Hostel Mess B"
    deadline = input("Pickup Deadline HH:MM (default: 20:00): ").strip() or "20:00"
    
    report = {
        "food_type": food_type,
        "quantity": quantity,
        "prep_time": prep_time,
        "temperature_c": temperature_c,
        "location": location,
        "pickup_deadline": deadline,
    }
    
    print("\n" + "=" * 70)
    print("Processing report through all agents...\n")
    
    flow = SutradharaFlow()
    result = flow.execute_flow(report)
    
    run_id = result["run_id"]
    final_decision = result.get("final_decision", {})
    trace = result.get("trace", {})
    
    print("=" * 70)
    print(f"\n✓ Run ID: {run_id}\n")
    
    print("FINAL DECISION:")
    print(f"  Action: {final_decision.get('action')}")
    print(f"  Recipient: {final_decision.get('recipient_name', 'N/A')}")
    print(f"  Pickup Time: {final_decision.get('pickup_time', 'N/A')}")
    print(f"  Explanation: {final_decision.get('explanation')}\n")
    
    print("TRACE SUMMARY:")
    if "stages" in trace:
        for agent, stage_data in trace["stages"].items():
            latency = stage_data.get("latency_ms", 0)
            status = stage_data.get("status", "unknown")
            print(f"  {agent:15s}: {status:10s} ({latency:6.1f} ms)")
    
    print("\n" + "=" * 70)
    
    if input("\nView full trace? (y/n): ").lower() == "y":
        print("\nFull Trace (JSON):")
        print(json.dumps(trace, indent=2, default=str))
    
    print()


def print_help():
    """Print help and documentation."""
    help_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║               FoodRescue-MAS: Help and Documentation                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROJECT OVERVIEW
────────────────
FoodRescue-MAS is a CrewAI-based multi-agent system for surplus food
redistribution. It uses specialized agents to make coordinated decisions
about validating, matching, assessing safety, and scheduling food pickups.

KEY COMPONENTS
──────────────
1. AGENTS (The Cast)
   • Eklavya (Intake & Validation) - Validates surplus reports
   • Arjuna (Demand & Matching) - Ranks compatible recipients
   • Dronacharya (Safety & Compliance) - Assesses safety with RAG
   • Chanakya (Logistics Manager) - Makes final decision and plan

2. ORCHESTRATION
   • Sutradhara (CrewAI Flow) - Manages flow, state, validation
   • Sukshmadarshini (Observer) - Tracks metrics and evaluation

3. INTERFACES
   • Sanjaya REST API - HTTP endpoints (localhost:8000)
   • Streamlit Dashboard - Web UI (localhost:8501)

4. DATA
   • Vyasa Generator - Creates synthetic test scenarios
   • Knowledge Base (FAISS) - Food safety rules for RAG
   • SQLite Recipients - Recipient organization database

MODES OF USE
────────────
a) EVALUATION (test_runner.py)
   - Generates 40 synthetic scenarios
   - Runs each through complete flow
   - Scores against ground truth
   - Outputs accuracy, latency, reliability metrics
   - Definition of Done: ≥75% accuracy, every verdict cited

b) REST API (api.py)
   - HTTP endpoints for integration
   - Submit reports programmatically
   - Query runs, recipients, metrics
   - Run evaluation suite remotely

c) WEB DASHBOARD (streamlit_dashboard.py)
   - Interactive report submission
   - Real-time decision feedback
   - Metrics visualization
   - RAG retrieval testing

d) COMMAND-LINE (this script)
   - Interactive single-report testing
   - Immediate feedback loop

FILES
─────
Core:
  schemas.py                 - Pydantic data models
  tools.py                   - Deterministic tool functions
  agents.py                  - The four specialized agents
  sutradhara_flow.py        - Orchestration logic
  sukshmadarshini_observer.py - Observability layer

Data:
  vyasa_generator.py         - Scenario generation
  rag_knowledge_base.py      - Food safety knowledge base
  food_categories.py         - Food type mappings

Interfaces:
  api.py                     - FastAPI backend
  streamlit_dashboard.py     - Streamlit UI
  test_runner.py            - Evaluation suite

EXAMPLE WORKFLOWS
─────────────────
1. Quick Evaluation:
   $ python test_runner.py
   
   Output: Accuracy, per-agent metrics, full report

2. Run API Server:
   $ python api.py
   
   Then use curl or Postman:
   POST http://localhost:8000/api/v1/reports
   GET http://localhost:8000/api/v1/evaluate/summary

3. Interactive Dashboard:
   $ streamlit run streamlit_dashboard.py
   
   - Submit reports via form
   - View run history
   - See live metrics

4. Programmatic Use:
   from sutradhara_flow import SutradharaFlow
   flow = SutradharaFlow()
   result = flow.execute_flow(report_dict)

DATA FLOW EXAMPLE
─────────────────
Input: Hostel Mess B reports 60 portions vegetable biryani
       at 58°C, pickup by 20:00

1. EKLAVYA: Validates fields, confirms location exists
2. ARJUNA: Queries recipients accepting cooked vegetables,
           ranks by distance and capacity
3. DRONACHARYA: Retrieves safety passages on cooked rice & hot holding,
                confirms temperature and time safe
4. CHANAKYA: Schedules pickup with top recipient, marks dispatch

Output: dispatch to Community Kitchen A at 18:15

METRICS TRACKED
───────────────
- End-to-End Accuracy: Final decision vs ground truth
- Per-Agent Accuracy: Each agent's performance independently
- Retrieval Quality: Relevance of RAG-retrieved evidence
- Latency: Total and per-agent timing
- Reliability: % complete runs, schema validation failures

DEFINITION OF DONE
──────────────────
✓ 40 scenarios run without crash
✓ ≥75% end-to-end accuracy
✓ Every safety verdict cites retrieved passage

Run evaluation and check:
$ python test_runner.py

Then look for "Definition of Done Check" section.

KEY CONCEPTS
────────────
• Schema Validation: Every agent output checked against Pydantic model
• One Retry: Failed schemas retried once, then stopped
• Evidence-Based: All safety decisions must cite knowledge base
• Deterministic Tools: No LLM in tools—pure functions for traceability
• Structured Traces: Every run fully logged and searchable

TROUBLESHOOTING
───────────────
Low accuracy?
→ Check Dronacharya's retrieval quality
→ Expand or improve knowledge base passages

Slow performance?
→ Normal: LLM calls are ~50-100ms each
→ 40 runs × 4 agents = ~2-5 minutes total

Import errors?
→ pip install -r requirements.txt

API not starting?
→ Port 8000 in use? Try: uvicorn api:app --port 8001

NEXT STEPS
──────────
Phase 2 Research Topics:
• Hierarchical agent architecture (manager-subordinate)
• Event-driven execution patterns
• LLM-as-Judge evaluation framework
• Communication protocol comparison (MCP, A2A, Blackboard)
• Multi-modal agent capabilities

For more details, see:
  README.md                 - Project overview
  SETUP_AND_RUNNING.md      - Installation and usage
  Inline code comments      - Implementation details

════════════════════════════════════════════════════════════════════════════════
"""
    print(help_text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye! 👋\n")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}\n")
        sys.exit(1)
