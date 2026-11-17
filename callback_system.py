"""
Callback System for Real-time Monitoring and Validation
Hooks for agent lifecycle events, tool execution, and data validation
"""

import json
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from enum import Enum
from enhanced_schemas import CallbackEvent, CallbackData
from guardrails_security import GuardrailValidator, SecurityLevel


class CallbackType(str, Enum):
    """Types of callbacks"""
    BEFORE_EVENT = "before"  # Pre-execution hooks
    AFTER_EVENT = "after"    # Post-execution hooks
    ON_ERROR = "error"       # Error handlers


class CallbackRegistry:
    """Registry for callback functions"""
    
    def __init__(self):
        self.callbacks: Dict[CallbackEvent, List[Callable]] = {}
        self.execution_log: List[Dict[str, Any]] = []
        self.guardrails = GuardrailValidator(SecurityLevel.STRICT)
    
    def register(self, event: CallbackEvent, callback: Callable):
        """Register a callback for an event"""
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)
        print(f"✓ Registered callback for {event.value}")
    
    def unregister(self, event: CallbackEvent, callback: Callable):
        """Unregister a callback"""
        if event in self.callbacks:
            self.callbacks[event].remove(callback)
    
    def trigger(self, event: CallbackEvent, data: CallbackData):
        """Trigger all callbacks for an event"""
        if event not in self.callbacks:
            return
        
        for callback in self.callbacks[event]:
            try:
                result = callback(data)
                self.execution_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "event": event.value,
                    "callback": callback.__name__,
                    "status": "success",
                    "result": str(result)
                })
            except Exception as e:
                self.execution_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "event": event.value,
                    "callback": callback.__name__,
                    "status": "error",
                    "error": str(e)
                })
    
    def get_log(self) -> List[Dict[str, Any]]:
        """Get callback execution log"""
        return self.execution_log


class AgentCallbacks:
    """Callbacks for agent lifecycle events"""
    
    def __init__(self, registry: CallbackRegistry):
        self.registry = registry
        self._register_callbacks()
    
    def _register_callbacks(self):
        """Register agent callbacks"""
        self.registry.register(CallbackEvent.AGENT_START, self.on_agent_start)
        self.registry.register(CallbackEvent.AGENT_COMPLETE, self.on_agent_complete)
        self.registry.register(CallbackEvent.ERROR, self.on_error)
    
    def on_agent_start(self, data: CallbackData):
        """Called when agent starts execution"""
        agent_id = data.agent_id
        run_id = data.run_id
        
        print(f"\n→ [START] Agent: {agent_id} (Run: {run_id})")
        print(f"  Timestamp: {data.timestamp}")
        
        return {"status": "started"}
    
    def on_agent_complete(self, data: CallbackData):
        """Called when agent completes execution"""
        agent_id = data.agent_id
        
        print(f"✓ [COMPLETE] Agent: {agent_id}")
        print(f"  Data: {data.data}")
        
        return {"status": "completed"}
    
    def on_error(self, data: CallbackData):
        """Called when agent encounters error"""
        agent_id = data.agent_id
        error = data.error
        
        print(f"✗ [ERROR] Agent: {agent_id}")
        print(f"  Error: {error}")
        
        return {"status": "error_handled"}


class ToolCallbacks:
    """Callbacks for tool execution"""
    
    def __init__(self, registry: CallbackRegistry):
        self.registry = registry
        self.guardrails = GuardrailValidator(SecurityLevel.STANDARD)
        self._register_callbacks()
    
    def _register_callbacks(self):
        """Register tool callbacks"""
        self.registry.register(CallbackEvent.TOOL_CALL, self.on_tool_call)
        self.registry.register(CallbackEvent.TOOL_RESULT, self.on_tool_result)
        self.registry.register(CallbackEvent.TOOL_ERROR, self.on_tool_error)
    
    def on_tool_call(self, data: CallbackData):
        """Called when tool is about to be called"""
        tool_name = data.data.get("tool_name")
        args = data.data.get("args")
        
        print(f"  → Tool: {tool_name}")
        
        # Validate input arguments
        if isinstance(args, dict):
            for key, value in args.items():
                if isinstance(value, str):
                    valid, violations = self.guardrails.validate_input(value, data.agent_id)
                    if not valid:
                        print(f"    ⚠ Input validation warning for {key}: {violations}")
        
        return {"status": "tool_ready"}
    
    def on_tool_result(self, data: CallbackData):
        """Called when tool returns result"""
        tool_name = data.data.get("tool_name")
        result = data.data.get("result")
        execution_time = data.data.get("execution_time_ms", 0)
        
        print(f"    ✓ Result received ({execution_time:.2f}ms)")
        
        # Validate output
        if isinstance(result, dict) and "error" in result:
            print(f"    ⚠ Tool error in result: {result['error']}")
        
        return {"status": "result_validated"}
    
    def on_tool_error(self, data: CallbackData):
        """Called when tool encounters error"""
        tool_name = data.data.get("tool_name")
        error = data.error
        
        print(f"    ✗ Tool error: {error}")
        
        return {"status": "error_handled"}


class DecisionCallbacks:
    """Callbacks for agent decisions"""
    
    def __init__(self, registry: CallbackRegistry):
        self.registry = registry
        self.guardrails = GuardrailValidator(SecurityLevel.STRICT)
        self._register_callbacks()
    
    def _register_callbacks(self):
        """Register decision callbacks"""
        self.registry.register(CallbackEvent.DECISION_MADE, self.on_decision)
        self.registry.register(CallbackEvent.STATE_CHANGED, self.on_state_change)
    
    def on_decision(self, data: CallbackData):
        """Called when agent makes a decision"""
        decision = data.data.get("decision")
        agent_id = data.agent_id
        
        print(f"  ⚖ Decision by {agent_id}: {decision.get('action', 'unknown')}")
        
        # Validate decision
        valid, issues = self.guardrails.validate_agent_decision(decision)
        if not valid:
            print(f"    ⚠ Decision validation issues: {issues}")
        
        return {"status": "decision_validated", "valid": valid}
    
    def on_state_change(self, data: CallbackData):
        """Called when agent state changes"""
        agent_id = data.agent_id
        changes = data.data.get("changes", {})
        
        print(f"  ↻ State updated by {agent_id}: {len(changes)} changes")
        
        return {"status": "state_updated"}


class ObservabilityCallbacks:
    """Callbacks for observability and tracing"""
    
    def __init__(self, registry: CallbackRegistry):
        self.registry = registry
        self.traces: Dict[str, List[Dict]] = {}
        self._register_callbacks()
    
    def _register_callbacks(self):
        """Register observability callbacks"""
        self.registry.register(CallbackEvent.AGENT_START, self.start_trace)
        self.registry.register(CallbackEvent.AGENT_COMPLETE, self.record_trace)
    
    def start_trace(self, data: CallbackData):
        """Start execution trace"""
        run_id = data.run_id
        agent_id = data.agent_id
        
        if run_id not in self.traces:
            self.traces[run_id] = []
        
        trace_entry = {
            "timestamp": data.timestamp,
            "agent_id": agent_id,
            "event": "start",
            "data": data.data
        }
        self.traces[run_id].append(trace_entry)
        
        return {"status": "trace_started"}
    
    def record_trace(self, data: CallbackData):
        """Record completion in trace"""
        run_id = data.run_id
        agent_id = data.agent_id
        
        if run_id not in self.traces:
            self.traces[run_id] = []
        
        trace_entry = {
            "timestamp": data.timestamp,
            "agent_id": agent_id,
            "event": "complete",
            "data": data.data
        }
        self.traces[run_id].append(trace_entry)
        
        return {"status": "trace_recorded"}
    
    def get_trace(self, run_id: str) -> List[Dict]:
        """Get execution trace for a run"""
        return self.traces.get(run_id, [])
    
    def get_all_traces(self) -> Dict[str, List[Dict]]:
        """Get all traces"""
        return self.traces


class MetricsCollector:
    """Collect metrics from callbacks"""
    
    def __init__(self, registry: CallbackRegistry):
        self.registry = registry
        self.metrics: Dict[str, Any] = {
            "agent_count": 0,
            "tool_calls": 0,
            "errors": 0,
            "total_latency_ms": 0,
            "decisions_made": 0
        }
        self._register_callbacks()
    
    def _register_callbacks(self):
        """Register metric collection callbacks"""
        self.registry.register(CallbackEvent.AGENT_START, self.count_agent)
        self.registry.register(CallbackEvent.TOOL_CALL, self.count_tool_call)
        self.registry.register(CallbackEvent.ERROR, self.count_error)
        self.registry.register(CallbackEvent.DECISION_MADE, self.count_decision)
    
    def count_agent(self, data: CallbackData):
        """Count agent execution"""
        self.metrics["agent_count"] += 1
        return {"agent_count": self.metrics["agent_count"]}
    
    def count_tool_call(self, data: CallbackData):
        """Count tool call"""
        self.metrics["tool_calls"] += 1
        return {"tool_calls": self.metrics["tool_calls"]}
    
    def count_error(self, data: CallbackData):
        """Count error"""
        self.metrics["errors"] += 1
        return {"errors": self.metrics["errors"]}
    
    def count_decision(self, data: CallbackData):
        """Count decision"""
        self.metrics["decisions_made"] += 1
        return {"decisions": self.metrics["decisions_made"]}
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics"""
        return self.metrics
    
    def print_summary(self):
        """Print metrics summary"""
        print("\n" + "=" * 70)
        print("METRICS SUMMARY")
        print("=" * 70)
        for metric, value in self.metrics.items():
            print(f"  {metric}: {value}")


class CallbackSystem:
    """Central callback system for the entire framework"""
    
    def __init__(self):
        self.registry = CallbackRegistry()
        self.agent_callbacks = AgentCallbacks(self.registry)
        self.tool_callbacks = ToolCallbacks(self.registry)
        self.decision_callbacks = DecisionCallbacks(self.registry)
        self.observability = ObservabilityCallbacks(self.registry)
        self.metrics = MetricsCollector(self.registry)
    
    def trigger_agent_start(self, agent_id: str, run_id: str, **kwargs):
        """Trigger agent start callback"""
        data = CallbackData(
            event_type=CallbackEvent.AGENT_START,
            agent_id=agent_id,
            run_id=run_id,
            data=kwargs
        )
        self.registry.trigger(CallbackEvent.AGENT_START, data)
    
    def trigger_agent_complete(self, agent_id: str, run_id: str, **kwargs):
        """Trigger agent complete callback"""
        data = CallbackData(
            event_type=CallbackEvent.AGENT_COMPLETE,
            agent_id=agent_id,
            run_id=run_id,
            data=kwargs
        )
        self.registry.trigger(CallbackEvent.AGENT_COMPLETE, data)
    
    def trigger_tool_call(self, agent_id: str, run_id: str, tool_name: str, args: Dict):
        """Trigger tool call callback"""
        data = CallbackData(
            event_type=CallbackEvent.TOOL_CALL,
            agent_id=agent_id,
            run_id=run_id,
            data={"tool_name": tool_name, "args": args}
        )
        self.registry.trigger(CallbackEvent.TOOL_CALL, data)
    
    def trigger_tool_result(self, agent_id: str, run_id: str, tool_name: str, 
                           result: Any, execution_time_ms: float):
        """Trigger tool result callback"""
        data = CallbackData(
            event_type=CallbackEvent.TOOL_RESULT,
            agent_id=agent_id,
            run_id=run_id,
            data={"tool_name": tool_name, "result": result, "execution_time_ms": execution_time_ms}
        )
        self.registry.trigger(CallbackEvent.TOOL_RESULT, data)
    
    def trigger_tool_error(self, agent_id: str, run_id: str, tool_name: str, error: str):
        """Trigger tool error callback"""
        data = CallbackData(
            event_type=CallbackEvent.TOOL_ERROR,
            agent_id=agent_id,
            run_id=run_id,
            data={"tool_name": tool_name},
            error=error
        )
        self.registry.trigger(CallbackEvent.TOOL_ERROR, data)
    
    def trigger_decision(self, agent_id: str, run_id: str, decision: Dict):
        """Trigger decision callback"""
        data = CallbackData(
            event_type=CallbackEvent.DECISION_MADE,
            agent_id=agent_id,
            run_id=run_id,
            data={"decision": decision}
        )
        self.registry.trigger(CallbackEvent.DECISION_MADE, data)
    
    def trigger_state_change(self, agent_id: str, run_id: str, changes: Dict):
        """Trigger state change callback"""
        data = CallbackData(
            event_type=CallbackEvent.STATE_CHANGED,
            agent_id=agent_id,
            run_id=run_id,
            data={"changes": changes}
        )
        self.registry.trigger(CallbackEvent.STATE_CHANGED, data)
    
    def trigger_error(self, agent_id: str, run_id: str, error: str):
        """Trigger error callback"""
        data = CallbackData(
            event_type=CallbackEvent.ERROR,
            agent_id=agent_id,
            run_id=run_id,
            error=error
        )
        self.registry.trigger(CallbackEvent.ERROR, data)
    
    def get_trace(self, run_id: str) -> List[Dict]:
        """Get execution trace"""
        return self.observability.get_trace(run_id)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get metrics"""
        return self.metrics.get_metrics()
    
    def print_report(self):
        """Print comprehensive report"""
        print("\n" + "=" * 70)
        print("CALLBACK SYSTEM REPORT")
        print("=" * 70)
        
        self.metrics.print_summary()
        
        print("\n" + "=" * 70)
        print("RECENT EXECUTIONS")
        print("=" * 70)
        
        log = self.registry.get_log()
        for entry in log[-10:]:  # Last 10
            print(f"  [{entry['timestamp']}] {entry['event']}: {entry['status']}")


# Global callback system
callback_system = CallbackSystem()


if __name__ == "__main__":
    # Demo
    print("=" * 70)
    print("CALLBACK SYSTEM DEMO")
    print("=" * 70)
    
    # Simulate agent execution
    run_id = "demo_run_001"
    
    print("\n[1] Agent Start")
    callback_system.trigger_agent_start("eklavya", run_id, food_type="biryani")
    
    print("\n[2] Tool Call")
    callback_system.trigger_tool_call("eklavya", run_id, "validate_schema", {"quantity": 60})
    
    print("\n[3] Tool Result")
    callback_system.trigger_tool_result("eklavya", run_id, "validate_schema", 
                                       {"valid": True}, 25.5)
    
    print("\n[4] Decision Made")
    callback_system.trigger_decision("eklavya", run_id, 
                                    {"action": "dispatch", "reason": "Valid food"})
    
    print("\n[5] Agent Complete")
    callback_system.trigger_agent_complete("eklavya", run_id, status="success")
    
    # Print report
    callback_system.print_report()
    
    # Print trace
    print("\n" + "=" * 70)
    print("EXECUTION TRACE")
    print("=" * 70)
    trace = callback_system.get_trace(run_id)
    for entry in trace:
        print(f"  {entry['timestamp']}: {entry['agent_id']} - {entry['event']}")
