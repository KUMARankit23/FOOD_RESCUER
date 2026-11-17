"""
Sanjaya: REST API and Streamlit UI.
Narrates each run to the user.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
import os
from pathlib import Path

from sutradhara_flow import SutradharaFlow
from sukshmadarshini_observer import SukshmadarshiniObserver
from vyasa_generator import generate_batch


app = FastAPI(title="FoodRescue-MAS API", version="0.1.0")

# Add CORS middleware to allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
flow = SutradharaFlow()
observer = SukshmadarshiniObserver()
run_history = {}


# Pydantic models for API
class SurplusReportRequest(BaseModel):
    food_type: str
    quantity: int
    prep_time: str
    temperature_c: float
    location: str
    pickup_deadline: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str


class RunResponse(BaseModel):
    run_id: str
    decision: Dict[str, Any]
    trace: Dict[str, Any]


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Service and dependency check."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/api/v1/reports", response_model=Dict[str, Any])
def submit_report(request: SurplusReportRequest):
    """
    Submit a surplus report, run the Flow, return the FinalDecision and run_id.
    """
    
    report_dict = request.dict()
    
    result = flow.execute_flow(report_dict)
    run_id = result["run_id"]
    
    # Store in history
    run_history[run_id] = result
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {
        "run_id": run_id,
        "final_decision": result.get("final_decision"),
    }


@app.get("/api/v1/runs")
def list_runs():
    """List past runs with status and latency."""
    
    runs_summary = []
    for run_id, result in run_history.items():
        trace = result.get("trace", {})
        final_decision = result.get("final_decision", {})
        
        runs_summary.append({
            "run_id": run_id,
            "status": trace.get("status", "unknown"),
            "decision_action": final_decision.get("action"),
            "recipient_id": final_decision.get("recipient_id"),
            "start_time": trace.get("start_time"),
            "end_time": trace.get("end_time"),
        })
    
    return {"runs": runs_summary}


@app.get("/api/v1/runs/{run_id}")
def get_run(run_id: str):
    """Full stored record of one run."""
    
    if run_id not in run_history:
        raise HTTPException(status_code=404, detail="Run not found")
    
    return run_history[run_id]


@app.get("/api/v1/runs/{run_id}/trace")
def get_run_trace(run_id: str):
    """Ordered agent trace with timestamps and tool calls."""
    
    if run_id not in run_history:
        raise HTTPException(status_code=404, detail="Run not found")
    
    trace = run_history[run_id].get("trace", {})
    
    return {
        "run_id": run_id,
        "trace": trace,
    }


@app.get("/api/v1/recipients")
def list_recipients():
    """List registered recipients."""
    
    from tools import RECIPIENTS_DB
    
    recipients = []
    for rid, data in RECIPIENTS_DB.items():
        recipients.append({
            "id": rid,
            "name": data["name"],
            "capacity": data["capacity"],
            "location": data["location"],
            "food_types": data["food_types"],
            "hours": data["hours"],
        })
    
    return {"recipients": recipients}


@app.post("/api/v1/scenarios/generate")
def generate_scenarios(count: int = 10):
    """Ask Vyasa for N new scenarios with ground truth."""
    
    if count > 100:
        count = 100
    
    scenarios = generate_batch(count)
    
    return {
        "count": len(scenarios),
        "scenarios": scenarios,
    }


@app.post("/api/v1/evaluate")
def evaluate_scenarios(count: int = 40):
    """Run all scenarios through the Flow and score them."""
    
    scenarios = generate_batch(count)
    results = []
    
    for scenario in scenarios:
        report = scenario["report"]
        ground_truth = scenario["ground_truth"]
        
        # Run through flow
        result = flow.execute_flow(report)
        run_id = result["run_id"]
        trace = result.get("trace", {})
        
        # Record with observer
        observer.record_run(run_id, trace, ground_truth)
        
        # Store result
        evaluation = observer.get_run_evaluation(run_id)
        results.append({
            "run_id": run_id,
            "action": result.get("final_decision", {}).get("action"),
            "expected_action": ground_truth.get("expected_action"),
            "accuracy": evaluation.get("end_to_end_accuracy") if evaluation else 0,
        })
    
    return {
        "total_evaluated": len(results),
        "results": results,
        "summary": observer.compute_summary_metrics(),
    }


@app.get("/api/v1/evaluate/summary")
def get_evaluation_summary():
    """Accuracy, latency and reliability figures."""
    
    return observer.compute_summary_metrics()


@app.get("/api/v1/safety/retrieve")
def retrieve_safety_passages(q: str):
    """Debug endpoint to test RAG retrieval directly."""
    
    from rag_knowledge_base import retrieve_passages
    
    results = retrieve_passages(q, k=3)
    
    return {
        "query": q,
        "passages": results,
    }


# ============================================================
# MAP TRACKING ENDPOINTS
# ============================================================

@app.get("/api/v1/map/tracking")
def get_tracking_data():
    """Get real-time tracking data for all active dispatches."""
    
    from map_tracking import calculate_route_stats, DONOR_LOCATIONS, RECIPIENTS_DB
    
    # Extract active dispatches from run history
    active_dispatches = []
    for run_id, result in run_history.items():
        final_decision = result.get("final_decision", {})
        if final_decision.get("action") == "dispatch":
            dispatch = {
                "run_id": run_id,
                "donor_location": result.get("trace", {}).get("input", {}).get("location", ""),
                "recipient_id": final_decision.get("recipient_id", ""),
                "recipient_name": final_decision.get("recipient_name", ""),
                "quantity": result.get("trace", {}).get("input", {}).get("quantity", 0),
                "status": "delivered",
                "created_at": result.get("trace", {}).get("start_time", ""),
            }
            active_dispatches.append(dispatch)
    
    # Get statistics
    stats = calculate_route_stats(active_dispatches)
    
    return {
        "dispatches": active_dispatches,
        "statistics": stats,
        "donors": [
            {
                "name": name,
                "coords": data["coords"],
                "icon_color": data["icon_color"]
            }
            for name, data in DONOR_LOCATIONS.items()
        ],
        "recipients": [
            {
                "id": rid,
                "name": data["name"],
                "coords": data["coords"],
                "capacity": data["capacity"],
                "icon_color": data["icon_color"]
            }
            for rid, data in RECIPIENTS_DB.items()
        ],
    }


@app.get("/api/v1/map/statistics")
def get_map_statistics():
    """Get aggregated statistics about routes and dispatches."""
    
    from map_tracking import calculate_route_stats
    
    # Build dispatch list from run history
    dispatches = []
    for run_id, result in run_history.items():
        final_decision = result.get("final_decision", {})
        if final_decision.get("action") == "dispatch":
            dispatch = {
                "run_id": run_id,
                "donor_location": result.get("trace", {}).get("input", {}).get("location", ""),
                "recipient_id": final_decision.get("recipient_id", ""),
                "status": "delivered",
                "quantity": result.get("trace", {}).get("input", {}).get("quantity", 0),
            }
            dispatches.append(dispatch)
    
    stats = calculate_route_stats(dispatches)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "statistics": stats,
    }


@app.get("/api/v1/map/history")
def get_dispatch_history():
    """Get historical dispatch data for heatmapping and analysis."""
    
    dispatch_history = []
    for run_id, result in run_history.items():
        final_decision = result.get("final_decision", {})
        if final_decision.get("action") == "dispatch":
            dispatch_history.append({
                "run_id": run_id,
                "donor_location": result.get("trace", {}).get("input", {}).get("location", ""),
                "recipient_id": final_decision.get("recipient_id", ""),
                "recipient_name": final_decision.get("recipient_name", ""),
                "quantity": result.get("trace", {}).get("input", {}).get("quantity", 0),
                "timestamp": result.get("trace", {}).get("start_time", ""),
            })
    
    return {
        "total_historical_dispatches": len(dispatch_history),
        "history": dispatch_history,
    }


@app.get("/api/v1/map/donors")
def get_donor_locations():
    """Get all donor locations."""
    
    from map_tracking import DONOR_LOCATIONS
    
    donors = [
        {
            "name": name,
            "coords": data["coords"],
            "icon_color": data["icon_color"],
            "icon": data["icon"],
        }
        for name, data in DONOR_LOCATIONS.items()
    ]
    
    return {
        "donors": donors,
        "total": len(donors),
    }


@app.get("/api/v1/map/recipients")
def get_recipient_locations():
    """Get all recipient locations with capacity and status."""
    
    from map_tracking import RECIPIENTS_DB
    
    recipients = [
        {
            "id": rid,
            "name": data["name"],
            "coords": data["coords"],
            "capacity": data["capacity"],
            "location": data["location"],
            "icon_color": data["icon_color"],
            "icon": data["icon"],
        }
        for rid, data in RECIPIENTS_DB.items()
    ]
    
    return {
        "recipients": recipients,
        "total": len(recipients),
    }


@app.post("/api/v1/map/generate-html")
def generate_map_html():
    """Generate HTML map file and return its content."""
    
    from map_tracking import (
        create_operation_map,
        add_heatmap,
        calculate_route_stats,
        export_map_html
    )
    
    # Build dispatch list from run history
    dispatches = []
    for run_id, result in run_history.items():
        final_decision = result.get("final_decision", {})
        if final_decision.get("action") == "dispatch":
            dispatch = {
                "run_id": run_id,
                "donor_location": result.get("trace", {}).get("input", {}).get("location", ""),
                "recipient_id": final_decision.get("recipient_id", ""),
                "recipient_name": final_decision.get("recipient_name", ""),
                "quantity": result.get("trace", {}).get("input", {}).get("quantity", 0),
                "status": "delivered",
                "created_at": result.get("trace", {}).get("start_time", ""),
            }
            dispatches.append(dispatch)
    
    # Create map
    m = create_operation_map(dispatches if dispatches else None)
    if dispatches:
        add_heatmap(m, dispatches)
    
    # Export
    filename = export_map_html(m, "operation_map_api.html")
    
    return {
        "status": "success",
        "filename": filename,
        "message": "Map HTML generated successfully",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Mount static files for React frontend - must be after all API routes
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
else:
    # Fallback: Create a simple index if static dir doesn't exist
    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        """Serve React index.html for all non-API routes."""
        index_path = Path(__file__).parent / "static" / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        return {"detail": "Static files not found. Ensure frontend is built and copied to /app/static"}
