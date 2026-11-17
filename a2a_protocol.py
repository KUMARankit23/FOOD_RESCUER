"""
A2A Protocol Implementation - Agent to Agent Communication
Standardized messaging between agents using official A2A pattern
"""

import json
import uuid
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from schemas import A2AMessage


class A2AProtocol:
    """Official A2A protocol implementation"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.message_queue: Dict[str, List[A2AMessage]] = {}
        self.message_log: List[A2AMessage] = []
        self.callbacks: Dict[str, List[Callable]] = {}
    
    def register_agent(self, agent_id: str, agent_name: str, framework: str, capabilities: List[str]):
        """Register agent for discovery"""
        self.agents[agent_id] = {
            "name": agent_name,
            "framework": framework,
            "capabilities": capabilities,
            "registered_at": datetime.now().isoformat()
        }
    
    def send_message(self, sender_id: str, sender_fw: str, receiver_id: str, receiver_fw: str, 
                    message_type: str, payload: Dict[str, Any]) -> A2AMessage:
        """Send A2A message"""
        message = A2AMessage(
            message_id=str(uuid.uuid4()),
            sender_agent=sender_id,
            sender_framework=sender_fw,
            receiver_agent=receiver_id,
            receiver_framework=receiver_fw,
            message_type=message_type,
            payload=payload,
            timestamp=datetime.now().isoformat()
        )
        
        if receiver_id not in self.message_queue:
            self.message_queue[receiver_id] = []
        
        self.message_queue[receiver_id].append(message)
        self.message_log.append(message)
        
        if receiver_id in self.callbacks:
            for callback in self.callbacks[receiver_id]:
                callback(message)
        
        return message
    
    def get_messages(self, agent_id: str) -> List[A2AMessage]:
        """Get messages for agent"""
        return self.message_queue.get(agent_id, [])
    
    def clear_messages(self, agent_id: str):
        """Clear processed messages"""
        if agent_id in self.message_queue:
            self.message_queue[agent_id] = []
    
    def register_callback(self, agent_id: str, callback: Callable):
        """Register message callback"""
        if agent_id not in self.callbacks:
            self.callbacks[agent_id] = []
        self.callbacks[agent_id].append(callback)
    
    def get_audit_trail(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get communication audit trail"""
        if agent_id:
            messages = [m for m in self.message_log 
                       if m.sender_agent == agent_id or m.receiver_agent == agent_id]
        else:
            messages = self.message_log
        
        return [m.dict() for m in messages]


# Global A2A protocol
a2a_protocol_instance = A2AProtocol()


def get_a2a_protocol() -> A2AProtocol:
    """Get global A2A protocol"""
    return a2a_protocol_instance

