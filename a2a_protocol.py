"""
Agent-to-Agent (A2A) Communication Protocol
Enables cross-framework communication between CrewAI and ADK agents
"""

import json
import uuid
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enhanced_schemas import A2AMessage, A2AMessageType, A2AAgent


class AgentRegistry:
    """Registry for agent discovery and management"""
    
    def __init__(self):
        self.agents: Dict[str, A2AAgent] = {}
        self.agent_endpoints: Dict[str, str] = {}
    
    def register_agent(self, agent: A2AAgent, endpoint: str):
        """Register an agent in the discovery service"""
        self.agents[agent.agent_id] = agent
        self.agent_endpoints[agent.agent_id] = endpoint
        print(f"✓ Registered {agent.framework.upper()} agent: {agent.agent_name}")
    
    def discover_agent(self, agent_id: str) -> Optional[A2AAgent]:
        """Discover an agent by ID"""
        return self.agents.get(agent_id)
    
    def discover_by_capability(self, capability: str) -> List[A2AAgent]:
        """Find agents with specific capability"""
        return [a for a in self.agents.values() if capability in a.capabilities]
    
    def list_agents(self) -> List[A2AAgent]:
        """List all registered agents"""
        return list(self.agents.values())


class A2AMessageRouter:
    """Routes messages between agents across frameworks"""
    
    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self.message_queue: Dict[str, List[A2AMessage]] = {}
        self.message_history: List[A2AMessage] = []
        self.callbacks: Dict[str, List[Callable]] = {}
    
    def create_message(
        self,
        sender_id: str,
        sender_framework: str,
        receiver_id: str,
        receiver_framework: str,
        message_type: A2AMessageType,
        payload: Dict[str, Any]
    ) -> A2AMessage:
        """Create an A2A message"""
        message = A2AMessage(
            message_id=str(uuid.uuid4()),
            sender_agent=sender_id,
            sender_framework=sender_framework,
            receiver_agent=receiver_id,
            receiver_framework=receiver_framework,
            message_type=message_type,
            payload=payload,
            timestamp=datetime.now().isoformat()
        )
        return message
    
    def send_message(self, message: A2AMessage) -> bool:
        """Send a message to an agent"""
        receiver_id = message.receiver_agent
        
        # Validate receiver exists
        receiver = self.registry.discover_agent(receiver_id)
        if not receiver:
            print(f"✗ Receiver agent {receiver_id} not found")
            return False
        
        # Route message based on framework
        if receiver.framework == "crewai":
            return self._route_to_crewai(message)
        elif receiver.framework == "adk":
            return self._route_to_adk(message)
        
        return False
    
    def _route_to_crewai(self, message: A2AMessage) -> bool:
        """Route message to CrewAI agent"""
        # Queue message for CrewAI agent
        if message.receiver_agent not in self.message_queue:
            self.message_queue[message.receiver_agent] = []
        
        self.message_queue[message.receiver_agent].append(message)
        self.message_history.append(message)
        
        print(f"✓ Routed message {message.message_id} to CrewAI agent {message.receiver_agent}")
        return True
    
    def _route_to_adk(self, message: A2AMessage) -> bool:
        """Route message to ADK agent"""
        # Queue message for ADK agent
        if message.receiver_agent not in self.message_queue:
            self.message_queue[message.receiver_agent] = []
        
        self.message_queue[message.receiver_agent].append(message)
        self.message_history.append(message)
        
        print(f"✓ Routed message {message.message_id} to ADK agent {message.receiver_agent}")
        return True
    
    def get_messages_for_agent(self, agent_id: str) -> List[A2AMessage]:
        """Get all pending messages for an agent"""
        return self.message_queue.get(agent_id, [])
    
    def clear_messages_for_agent(self, agent_id: str):
        """Clear processed messages for an agent"""
        if agent_id in self.message_queue:
            self.message_queue[agent_id] = []
    
    def register_callback(self, agent_id: str, callback: Callable):
        """Register a callback for agent messages"""
        if agent_id not in self.callbacks:
            self.callbacks[agent_id] = []
        self.callbacks[agent_id].append(callback)
    
    def get_message_history(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get message history for audit trail"""
        if agent_id:
            messages = [m for m in self.message_history 
                       if m.sender_agent == agent_id or m.receiver_agent == agent_id]
        else:
            messages = self.message_history
        
        return [json.loads(m.model_dump_json()) for m in messages]


class A2AProtocol:
    """Main A2A Protocol handler"""
    
    def __init__(self):
        self.registry = AgentRegistry()
        self.router = A2AMessageRouter(self.registry)
    
    def register_crewai_agent(self, agent_id: str, agent_name: str, 
                             capabilities: List[str], 
                             input_schema: Dict, 
                             output_schema: Dict):
        """Register a CrewAI agent"""
        agent = A2AAgent(
            agent_id=agent_id,
            agent_name=agent_name,
            framework="crewai",
            capabilities=capabilities,
            input_schema=input_schema,
            output_schema=output_schema
        )
        self.registry.register_agent(agent, f"crewai://{agent_id}")
    
    def register_adk_agent(self, agent_id: str, agent_name: str,
                          capabilities: List[str],
                          input_schema: Dict,
                          output_schema: Dict):
        """Register an ADK agent"""
        agent = A2AAgent(
            agent_id=agent_id,
            agent_name=agent_name,
            framework="adk",
            capabilities=capabilities,
            input_schema=input_schema,
            output_schema=output_schema
        )
        self.registry.register_agent(agent, f"adk://{agent_id}")
    
    def send_request(self, sender_id: str, sender_fw: str,
                    receiver_id: str, receiver_fw: str,
                    payload: Dict[str, Any]) -> A2AMessage:
        """Send a request message"""
        message = self.router.create_message(
            sender_id=sender_id,
            sender_framework=sender_fw,
            receiver_id=receiver_id,
            receiver_framework=receiver_fw,
            message_type=A2AMessageType.REQUEST,
            payload=payload
        )
        self.router.send_message(message)
        return message
    
    def send_response(self, sender_id: str, sender_fw: str,
                     receiver_id: str, receiver_fw: str,
                     payload: Dict[str, Any]) -> A2AMessage:
        """Send a response message"""
        message = self.router.create_message(
            sender_id=sender_id,
            sender_framework=sender_fw,
            receiver_id=receiver_id,
            receiver_framework=receiver_fw,
            message_type=A2AMessageType.RESPONSE,
            payload=payload
        )
        self.router.send_message(message)
        return message
    
    def send_state_update(self, sender_id: str, sender_fw: str,
                         receiver_id: str, receiver_fw: str,
                         state: Dict[str, Any]) -> A2AMessage:
        """Send a state update message"""
        message = self.router.create_message(
            sender_id=sender_id,
            sender_framework=sender_fw,
            receiver_id=receiver_id,
            receiver_framework=receiver_fw,
            message_type=A2AMessageType.STATE_UPDATE,
            payload={"state": state}
        )
        self.router.send_message(message)
        return message
    
    def discover_agents_with_capability(self, capability: str) -> List[A2AAgent]:
        """Discover agents by capability"""
        return self.registry.discover_by_capability(capability)
    
    def get_audit_trail(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get audit trail of all A2A communications"""
        return self.router.get_message_history(agent_id)


# Singleton instance
a2a_protocol = A2AProtocol()


if __name__ == "__main__":
    # Example usage
    protocol = A2AProtocol()
    
    # Register agents
    protocol.register_crewai_agent(
        "eklavya_crew",
        "Eklavya Intake Agent (CrewAI)",
        ["validate", "intake"],
        {"type": "surplus_report"},
        {"type": "validated_record"}
    )
    
    protocol.register_adk_agent(
        "arjuna_adk",
        "Arjuna Matching Agent (ADK)",
        ["matching", "ranking"],
        {"type": "validated_record"},
        {"type": "ranked_matches"}
    )
    
    # Send a message
    msg = protocol.send_request(
        sender_id="eklavya_crew",
        sender_fw="crewai",
        receiver_id="arjuna_adk",
        receiver_fw="adk",
        payload={
            "validated_record": {
                "food_type": "biryani",
                "quantity": 60
            }
        }
    )
    
    print(f"\n✓ Message sent: {msg.message_id}")
    print(f"✓ Agents discovered: {len(protocol.registry.list_agents())}")
