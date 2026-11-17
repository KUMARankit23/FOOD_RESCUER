"""
WebSocket Real-Time Tracking
Live updates for picker locations and status changes
"""

import asyncio
import json
from typing import Dict, List, Set, Any
from datetime import datetime


class WebSocketManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[Any]] = {}
        self.location_history: Dict[str, List[Dict[str, Any]]] = {}
        self.status_updates: Dict[str, List[Dict[str, Any]]] = {}
    
    async def connect(self, client_id: str, websocket):
        """Connect client"""
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
    
    async def disconnect(self, client_id: str, websocket):
        """Disconnect client"""
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
    
    async def broadcast_location(self, job_id: str, picker_id: str, latitude: float, 
                                longitude: float, accuracy: float):
        """Broadcast picker location update"""
        
        location_data = {
            "type": "location_update",
            "job_id": job_id,
            "picker_id": picker_id,
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy,
            "timestamp": datetime.now().isoformat()
        }
        
        if job_id not in self.location_history:
            self.location_history[job_id] = []
        self.location_history[job_id].append(location_data)
        
        await self._broadcast_to_run(job_id, location_data)
    
    async def broadcast_status_update(self, run_id: str, job_id: str, status: str, details: Dict[str, Any]):
        """Broadcast status update"""
        
        status_data = {
            "type": "status_update",
            "run_id": run_id,
            "job_id": job_id,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        if run_id not in self.status_updates:
            self.status_updates[run_id] = []
        self.status_updates[run_id].append(status_data)
        
        await self._broadcast_to_run(run_id, status_data)
    
    async def broadcast_agent_decision(self, run_id: str, agent: str, decision: Dict[str, Any]):
        """Broadcast agent decision"""
        
        decision_data = {
            "type": "agent_decision",
            "run_id": run_id,
            "agent": agent,
            "decision": decision,
            "timestamp": datetime.now().isoformat()
        }
        
        await self._broadcast_to_run(run_id, decision_data)
    
    async def _broadcast_to_run(self, run_id: str, message: Dict[str, Any]):
        """Broadcast message to all clients watching this run"""
        if run_id in self.active_connections:
            for websocket in self.active_connections[run_id]:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    print(f"Error broadcasting to {run_id}: {e}")
    
    def get_location_history(self, job_id: str) -> List[Dict[str, Any]]:
        """Get location history for a job"""
        return self.location_history.get(job_id, [])
    
    def get_status_history(self, run_id: str) -> List[Dict[str, Any]]:
        """Get status update history for a run"""
        return self.status_updates.get(run_id, [])
    
    def get_last_location(self, job_id: str) -> Dict[str, Any]:
        """Get last known location"""
        history = self.location_history.get(job_id, [])
        return history[-1] if history else None


# Global WebSocket manager
ws_manager = WebSocketManager()


def get_ws_manager() -> WebSocketManager:
    """Get global WebSocket manager"""
    return ws_manager
