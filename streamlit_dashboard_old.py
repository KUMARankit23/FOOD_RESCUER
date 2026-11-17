"""
Sanjaya UI: Streamlit dashboard for FoodRescue-MAS.
Shows runs, traces, and performance metrics.
"""

import streamlit as st
import json
import requests
from datetime import datetime
from sutradhara_flow import SutradharaFlow
from sukshmadarshini_observer import SukshmadarshiniObserver


st.set_page_config(page_title="FoodRescue-MAS", layout="wide")

st.title("🍛 FoodRescue-MAS Dashboard")
st.markdown("*Eight figures from the epics, one mission: no plate left behind.*")

# Initialize session state
if "flow" not in st.session_state:
    st.session_state.flow = SutradharaFlow()
    st.session_state.observer = SukshmadarshiniObserver()

flow = st.session_state.flow
observer = st.session_state.observer

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Submit Report", "View Runs", "Metrics", "Map Tracking", "RAG Test"])

# ============================================================
# PAGE 1: Submit Report
# ============================================================
if page == "Submit Report":
    st.header("📋 Submit Surplus Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        food_type = st.selectbox(
            "Food Type",
            ["vegetable biryani", "chicken curry", "rice", "bread", "dairy dessert"]
        )
        quantity = st.slider("Quantity (portions)", 10, 200, 60)
        prep_time = st.text_input("Prep Time (HH:MM)", "14:00")
    
    with col2:
        temperature_c = st.slider("Current Temperature (°C)", 5, 85, 58)
        location = st.selectbox(
            "Location",
            ["Hostel Mess A", "Hostel Mess B", "Canteen", "Event Hall", "Sports Complex"]
        )
        pickup_deadline = st.text_input("Pickup Deadline (HH:MM)", "20:00")
    
    if st.button("Submit Report", key="submit_btn", type="primary"):
        with st.spinner("Processing through all agents..."):
            report = {
                "food_type": food_type,
                "quantity": quantity,
                "prep_time": prep_time,
                "temperature_c": temperature_c,
                "location": location,
                "pickup_deadline": pickup_deadline,
            }
            
            result = flow.execute_flow(report)
            run_id = result["run_id"]
            
            # Store for later view
            if "last_run_id" not in st.session_state:
                st.session_state.last_run_id = run_id
            
            st.success(f"✓ Report processed. Run ID: {run_id}")
            
            # Show result
            final_decision = result.get("final_decision", {})
            st.subheader("Final Decision")
            
            action = final_decision.get("action", "unknown")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Action", action)
            with col2:
                st.metric("Recipient", final_decision.get("recipient_name", "N/A"))
            with col3:
                st.metric("Pickup Time", final_decision.get("pickup_time", "N/A"))
            
            st.info(final_decision.get("explanation", "No explanation provided."))
            
            # Show trace
            if st.checkbox("Show Trace Details"):
                trace = result.get("trace", {})
                st.json(trace)


# ============================================================
# PAGE 2: View Runs
# ============================================================
elif page == "View Runs":
    st.header("📊 View Past Runs")
    
    if flow.run_log:
        run_ids = list(flow.run_log.keys())
        selected_run = st.selectbox("Select Run", run_ids)
        
        if selected_run:
            run_data = flow.run_log[selected_run]
            
            st.subheader(f"Run: {selected_run}")
            
            # Summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Status", run_data.get("status", "unknown"))
            with col2:
                start = run_data.get("start_time", "N/A")
                st.metric("Start Time", start[:16] if isinstance(start, str) else "N/A")
            with col3:
                stages = run_data.get("stages", {})
                total_latency = sum(s.get("latency_ms", 0) for s in stages.values())
                st.metric("Total Latency", f"{total_latency:.1f} ms")
            
            # Agent breakdown
            st.subheader("Agent Execution")
            if "stages" in run_data:
                stages_df = []
                for agent, stage_data in run_data["stages"].items():
                    stages_df.append({
                        "Agent": agent,
                        "Status": stage_data.get("status", "unknown"),
                        "Latency (ms)": stage_data.get("latency_ms", 0),
                    })
                st.table(stages_df)
            
            # Full trace
            if st.checkbox("Show Full Trace"):
                st.json(run_data)
    else:
        st.info("No runs recorded yet. Submit a report first.")


# ============================================================
# PAGE 3: Metrics & Evaluation
# ============================================================
elif page == "Metrics":
    st.header("📈 Performance Metrics")
    
    if flow.run_log:
        # Compute metrics
        metrics = observer.compute_summary_metrics()
        
        if metrics:
            st.subheader("Summary Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Runs", metrics.get("total_runs", 0))
            with col2:
                acc = metrics.get("end_to_end_accuracy", 0)
                st.metric("E2E Accuracy", f"{acc:.1%}")
            with col3:
                latency = metrics.get("average_latency_ms", 0)
                st.metric("Avg Latency", f"{latency:.0f} ms")
            with col4:
                rel = metrics.get("reliability", 0)
                st.metric("Reliability", f"{rel:.1%}")
            
            st.subheader("Per-Agent Accuracy")
            agent_acc = metrics.get("per_agent_accuracy", {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Eklavya (Intake)", f"{agent_acc.get('eklavya_intake', 0):.1%}")
            with col2:
                st.metric("Arjuna (Matching)", f"{agent_acc.get('arjuna_matching', 0):.1%}")
            with col3:
                st.metric("Dronacharya (Safety)", f"{agent_acc.get('dronacharya_safety', 0):.1%}")
            
            st.subheader("Retrieval Quality")
            ret_qual = metrics.get("retrieval_quality", 0)
            st.progress(ret_qual, text=f"{ret_qual:.1%}")
            
            st.subheader("Definition of Done")
            col1, col2, col3 = st.columns(3)
            with col1:
                done_40 = metrics.get("total_runs", 0) >= 40
                st.metric("40+ Runs", "✓" if done_40 else "✗")
            with col2:
                done_acc = metrics.get("end_to_end_accuracy", 0) >= 0.75
                st.metric("≥75% Accuracy", "✓" if done_acc else "✗")
            with col3:
                done_cited = metrics.get("retrieval_quality", 0) > 0
                st.metric("Cited Evidence", "✓" if done_cited else "✗")
        else:
            st.info("Run some scenarios first to see metrics.")
    else:
        st.info("No runs recorded yet.")


# ============================================================
# PAGE 4: Map Tracking
# ============================================================
elif page == "Map Tracking":
    st.header("🗺️ Real-Time Map Tracking")
    
    st.markdown("""
    Track food rescue operations in real-time:
    - 🔴 **Red Pins**: Food donor locations
    - 🟢 **Green Pins**: Recipient locations  
    - 🔵 **Blue Lines**: Active delivery routes
    - 📊 **Statistics**: Distance, status, and performance metrics
    """)
    
    from map_tracking import (
        create_operation_map, 
        add_heatmap, 
        calculate_route_stats,
        export_map_html,
        SAMPLE_DISPATCH_HISTORY
    )
    
    # Get active dispatches from run log
    active_dispatches = []
    for run_id, run_data in flow.run_log.items():
        final_decision = run_data.get("final_decision", {})
        if final_decision.get("action") == "dispatch":
            dispatch = {
                "run_id": run_id,
                "donor_location": run_data.get("input", {}).get("location", ""),
                "recipient_id": final_decision.get("recipient_id", ""),
                "recipient_name": final_decision.get("recipient_name", ""),
                "quantity": run_data.get("input", {}).get("quantity", 0),
                "status": "delivered",
                "created_at": run_data.get("start_time", ""),
            }
            active_dispatches.append(dispatch)
    
    # Use sample data if no real dispatches
    if not active_dispatches:
        active_dispatches = SAMPLE_DISPATCH_HISTORY
    
    # Create map
    m = create_operation_map(active_dispatches)
    add_heatmap(m, active_dispatches)
    
    # Display map in Streamlit
    st.subheader("Live Operation Map")
    st.components.v1.html(m._repr_html_(), height=600, scrolling=False)
    
    # Display statistics
    stats = calculate_route_stats(active_dispatches)
    
    st.subheader("📊 Operation Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Dispatches", stats["total_dispatches"])
    with col2:
        st.metric("Distance Covered", f"{stats['total_distance_km']} km")
    with col3:
        st.metric("Active Routes", stats.get("active_dispatches", 0))
    with col4:
        st.metric("Delivered", stats.get("delivered", 0))
    
    # Status breakdown
    st.subheader("Dispatch Status Distribution")
    status_dist = stats["status_distribution"]
    
    col1, col2, col3 = st.columns(3)
    statuses = ["pending", "in_transit", "delivered"]
    colors = ["⏳", "🚚", "✓"]
    
    for i, (status, emoji) in enumerate(zip(statuses, colors)):
        count = status_dist.get(status, 0)
        if i == 0:
            st.metric(f"{emoji} Pending", count, col_number=col1)
        elif i == 1:
            st.metric(f"{emoji} In Transit", count, col_number=col2)
        else:
            st.metric(f"{emoji} Delivered", count, col_number=col3)
    
    # Dispatch details table
    st.subheader("Recent Dispatches")
    if active_dispatches:
        dispatch_data = []
        for d in active_dispatches[:10]:
            dispatch_data.append({
                "Run ID": d["run_id"],
                "From": d["donor_location"],
                "To": d["recipient_name"],
                "Quantity": d["quantity"],
                "Status": d["status"],
                "Time": d.get("created_at", "N/A")[:16] if isinstance(d.get("created_at"), str) else "N/A",
            })
        
        st.dataframe(dispatch_data, use_container_width=True)
    else:
        st.info("No dispatches yet. Submit reports to populate the map.")
    
    # Download map
    if st.button("📥 Download Map as HTML"):
        html_file = export_map_html(m, "operation_map.html")
        with open(html_file, "r") as f:
            st.download_button(
                label="Download",
                data=f.read(),
                file_name="operation_map.html",
                mime="text/html"
            )


# ============================================================
# PAGE 5: RAG Test
# ============================================================
elif page == "RAG Test":
    st.header("🔍 Test RAG Retrieval")
    
    st.markdown("Test the Safety Agent's RAG retrieval directly.")
    
    query = st.text_input("Enter search query:", "cooked meat temperature holding")
    
    if st.button("Retrieve Passages"):
        from rag_knowledge_base import retrieve_passages
        
        passages = retrieve_passages(query, k=3)
        
        st.subheader("Retrieved Passages")
        for i, passage in enumerate(passages, 1):
            with st.expander(f"[{passage['id']}] {passage['title']}", expanded=(i==1)):
                st.write(passage["text"])


st.sidebar.markdown("---")
st.sidebar.markdown("**FoodRescue-MAS**  \nMulti-Agent System for Food Redistribution")
st.sidebar.markdown("Built with CrewAI, RAG, FastAPI, and Streamlit")
