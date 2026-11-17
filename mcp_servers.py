"""
Real MCP (Model Context Protocol) Tool Servers
Each server exposes tools that agents can invoke via standardized MCP protocol
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class MCPToolSchema:
    """Tool schema for MCP"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class RecipientDatabaseServer:
    """MCP Server: Recipient Database Tools"""
    
    def __init__(self):
        self.name = "recipient_database_server"
        self.tools = self._define_tools()
    
    def _define_tools(self) -> Dict[str, MCPToolSchema]:
        """Define available tools"""
        from tools import query_recipients, get_recipient_details, lookup_location
        
        return {
            "search_recipients": MCPToolSchema(
                name="search_recipients",
                description="Search for recipient organizations matching food category",
                input_schema={
                    "type": "object",
                    "properties": {
                        "food_category": {"type": "string", "description": "Food category (e.g., 'cooked_veg', 'rice', 'meat')"},
                        "quantity": {"type": "integer", "description": "Quantity needed"},
                        "max_results": {"type": "integer", "description": "Max results to return", "default": 5}
                    },
                    "required": ["food_category"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "recipients": {"type": "array"}
                    }
                }
            ),
            "get_recipient_capacity": MCPToolSchema(
                name="get_recipient_capacity",
                description="Get capacity and current availability of a recipient",
                input_schema={
                    "type": "object",
                    "properties": {
                        "recipient_id": {"type": "string"}
                    },
                    "required": ["recipient_id"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "recipient_id": {"type": "string"},
                        "capacity": {"type": "integer"},
                        "current_occupancy": {"type": "integer"},
                        "available_space": {"type": "integer"}
                    }
                }
            ),
            "get_recipient_details": MCPToolSchema(
                name="get_recipient_details",
                description="Get detailed information about a recipient",
                input_schema={
                    "type": "object",
                    "properties": {
                        "recipient_id": {"type": "string"}
                    },
                    "required": ["recipient_id"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "location": {"type": "string"},
                        "food_preferences": {"type": "array"},
                        "dietary_restrictions": {"type": "array"},
                        "staff_trained": {"type": "boolean"}
                    }
                }
            ),
            "calculate_distance": MCPToolSchema(
                name="calculate_distance",
                description="Calculate distance between donor and recipient",
                input_schema={
                    "type": "object",
                    "properties": {
                        "donor_location": {"type": "string"},
                        "recipient_id": {"type": "string"}
                    },
                    "required": ["donor_location", "recipient_id"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "distance_km": {"type": "number"},
                        "travel_time_minutes": {"type": "number"}
                    }
                }
            )
        }
    
    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        from tools import query_recipients, distance_km
        
        if tool_name == "search_recipients":
            recipients = query_recipients(args["food_category"])
            return {"status": "success", "recipients": recipients}
        
        elif tool_name == "get_recipient_capacity":
            recipient_id = args["recipient_id"]
            # Mock data
            return {
                "status": "success",
                "recipient_id": recipient_id,
                "capacity": 200,
                "current_occupancy": 50,
                "available_space": 150
            }
        
        elif tool_name == "get_recipient_details":
            recipient_id = args["recipient_id"]
            # Mock implementation
            return {
                "status": "success",
                "id": recipient_id,
                "name": "Community Kitchen",
                "location": "Downtown",
                "food_preferences": ["all"],
                "dietary_restrictions": [],
                "staff_trained": True
            }
        
        elif tool_name == "calculate_distance":
            dist = distance_km(args["donor_location"], args["recipient_id"])
            return {
                "status": "success",
                "distance_km": dist,
                "travel_time_minutes": int(dist * 2)  # ~2min per km
            }


class FoodSafetyKnowledgeServer:
    """MCP Server: Food Safety Knowledge Base"""
    
    def __init__(self):
        self.name = "food_safety_knowledge_server"
        self.tools = self._define_tools()
    
    def _define_tools(self) -> Dict[str, MCPToolSchema]:
        """Define available tools"""
        return {
            "retrieve_food_safety_guidelines": MCPToolSchema(
                name="retrieve_food_safety_guidelines",
                description="Retrieve food safety guidelines using RAG",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Safety query"},
                        "top_k": {"type": "integer", "description": "Number of results", "default": 3}
                    },
                    "required": ["query"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "passages": {"type": "array"}
                    }
                }
            ),
            "get_temperature_requirements": MCPToolSchema(
                name="get_temperature_requirements",
                description="Get temperature requirements for a food type",
                input_schema={
                    "type": "object",
                    "properties": {
                        "food_type": {"type": "string"},
                        "storage_type": {"type": "string", "enum": ["hot", "cold", "room_temp"]}
                    },
                    "required": ["food_type"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "food_type": {"type": "string"},
                        "min_temperature_c": {"type": "number"},
                        "max_temperature_c": {"type": "number"},
                        "max_holding_hours": {"type": "number"},
                        "notes": {"type": "string"}
                    }
                }
            ),
            "check_allergens": MCPToolSchema(
                name="check_allergens",
                description="Check and verify allergen information",
                input_schema={
                    "type": "object",
                    "properties": {
                        "food_description": {"type": "string"}
                    },
                    "required": ["food_description"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "common_allergens": {"type": "array"},
                        "warning": {"type": "string"}
                    }
                }
            )
        }
    
    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        from rag_system import get_rag_system
        
        if tool_name == "retrieve_food_safety_guidelines":
            rag = get_rag_system()
            passages = rag.retrieve(args["query"], k=args.get("top_k", 3))
            return {
                "status": "success",
                "passages": passages
            }
        
        elif tool_name == "get_temperature_requirements":
            # Mock temperature data
            temps = {
                "cooked_veg": {"min": 57, "max": 65, "hours": 4},
                "rice": {"min": 60, "max": 70, "hours": 3},
                "meat": {"min": 74, "max": 82, "hours": 3},
                "dairy": {"min": 2, "max": 5, "hours": 48}
            }
            food = args["food_type"].lower()
            temp_data = temps.get(food, {"min": 57, "max": 65, "hours": 4})
            
            return {
                "status": "success",
                "food_type": args["food_type"],
                "min_temperature_c": temp_data["min"],
                "max_temperature_c": temp_data["max"],
                "max_holding_hours": temp_data["hours"],
                "notes": "Keep at required temperature throughout holding period"
            }
        
        elif tool_name == "check_allergens":
            # Mock allergen check
            allergens = ["peanuts", "milk", "eggs", "fish"]
            return {
                "status": "success",
                "common_allergens": allergens,
                "warning": "Verify allergen information with donor before dispatch"
            }


class LogisticsServer:
    """MCP Server: Location and Logistics Tools"""
    
    def __init__(self):
        self.name = "logistics_server"
        self.tools = self._define_tools()
    
    def _define_tools(self) -> Dict[str, MCPToolSchema]:
        """Define available tools"""
        return {
            "estimate_pickup_feasibility": MCPToolSchema(
                name="estimate_pickup_feasibility",
                description="Estimate if pickup is feasible given time constraints",
                input_schema={
                    "type": "object",
                    "properties": {
                        "recipient_id": {"type": "string"},
                        "deadline": {"type": "string", "description": "Pickup deadline (HH:MM)"}
                    },
                    "required": ["recipient_id", "deadline"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "feasible": {"type": "boolean"},
                        "scheduled_time": {"type": "string"},
                        "notes": {"type": "string"}
                    }
                }
            ),
            "find_alternative_recipients": MCPToolSchema(
                name="find_alternative_recipients",
                description="Find alternative recipients if primary is unavailable",
                input_schema={
                    "type": "object",
                    "properties": {
                        "food_type": {"type": "string"},
                        "quantity": {"type": "integer"},
                        "exclude_ids": {"type": "array"}
                    },
                    "required": ["food_type", "quantity"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "alternatives": {"type": "array"}
                    }
                }
            )
        }
    
    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        from tools import schedule_pickup, query_recipients
        
        if tool_name == "estimate_pickup_feasibility":
            schedule = schedule_pickup(args["recipient_id"], args["deadline"])
            return {
                "status": "success",
                "feasible": schedule["available"],
                "scheduled_time": schedule.get("scheduled_time", "N/A"),
                "notes": "Feasibility check complete"
            }
        
        elif tool_name == "find_alternative_recipients":
            recipients = query_recipients(args["food_type"])
            exclude = set(args.get("exclude_ids", []))
            alternatives = [r for r in recipients if r.get("recipient_id") not in exclude]
            return {
                "status": "success",
                "alternatives": alternatives[:3]  # Top 3
            }


class MCPServerManager:
    """Manager for all MCP servers"""
    
    def __init__(self):
        self.servers = {
            "recipient_database": RecipientDatabaseServer(),
            "food_safety": FoodSafetyKnowledgeServer(),
            "logistics": LogisticsServer()
        }
    
    def list_servers(self) -> List[str]:
        """List available servers"""
        return list(self.servers.keys())
    
    def list_tools(self, server_name: str) -> Dict[str, MCPToolSchema]:
        """List tools for a server"""
        if server_name not in self.servers:
            return {}
        return self.servers[server_name].tools
    
    def execute_tool(self, server_name: str, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool on a server"""
        if server_name not in self.servers:
            return {"status": "error", "message": f"Server {server_name} not found"}
        
        server = self.servers[server_name]
        if tool_name not in server.tools:
            return {"status": "error", "message": f"Tool {tool_name} not found"}
        
        try:
            return server.execute_tool(tool_name, args)
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Global MCP manager
mcp_manager = MCPServerManager()


def get_mcp_manager() -> MCPServerManager:
    """Get global MCP manager"""
    return mcp_manager
