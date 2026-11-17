"""
MCP (Model Context Protocol) Integration
External tool connections for web search, database lookup, file parsing, etc.
"""

import json
import requests
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime
from enhanced_schemas import MCPToolDefinition, MCPToolResult


class MCPServer:
    """Base class for MCP-compliant servers"""
    
    def __init__(self, server_name: str, server_type: str):
        self.server_name = server_name
        self.server_type = server_type
        self.connected = False
        self.tools: Dict[str, MCPToolDefinition] = {}
    
    def connect(self) -> bool:
        """Connect to MCP server"""
        raise NotImplementedError
    
    def disconnect(self) -> bool:
        """Disconnect from MCP server"""
        raise NotImplementedError
    
    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> MCPToolResult:
        """Execute a tool on this server"""
        raise NotImplementedError
    
    def list_tools(self) -> List[MCPToolDefinition]:
        """List available tools"""
        return list(self.tools.values())


class WebSearchMCPServer(MCPServer):
    """MCP Server for web search (SerpAPI integration)"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("web_search_mcp", "external_api")
        self.api_key = api_key or "demo_key"
        self.base_url = "https://serpapi.com/search"
        self._define_tools()
    
    def _define_tools(self):
        """Define available tools"""
        self.tools["search_web"] = MCPToolDefinition(
            tool_name="search_web",
            tool_type="external_api",
            mcp_server="web_search_mcp",
            description="Search the web for information",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "num_results": {"type": "integer", "description": "Number of results (max 10)"}
                },
                "required": ["query"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "link": {"type": "string"},
                                "snippet": {"type": "string"}
                            }
                        }
                    }
                }
            }
        )
        
        self.tools["search_news"] = MCPToolDefinition(
            tool_name="search_news",
            tool_type="external_api",
            mcp_server="web_search_mcp",
            description="Search for recent news articles",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "News search query"},
                    "days_back": {"type": "integer", "description": "Days to search back"}
                },
                "required": ["query"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "articles": {"type": "array"}
                }
            }
        )
    
    def connect(self) -> bool:
        """Connect to web search API"""
        try:
            # Test connection with demo query
            print(f"✓ Connecting to {self.server_name}...")
            self.connected = True
            print(f"✓ Connected to web search API")
            return True
        except Exception as e:
            print(f"✗ Failed to connect: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from web search API"""
        self.connected = False
        print(f"✓ Disconnected from {self.server_name}")
        return True
    
    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> MCPToolResult:
        """Execute web search tool"""
        start_time = datetime.now()
        
        try:
            if not self.connected:
                raise ConnectionError("Not connected to web search server")
            
            if tool_name == "search_web":
                return self._search_web(args)
            elif tool_name == "search_news":
                return self._search_news(args)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        
        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            return MCPToolResult(
                tool_name=tool_name,
                status="error",
                result={},
                execution_time_ms=elapsed,
                error_message=str(e)
            )
    
    def _search_web(self, args: Dict[str, Any]) -> MCPToolResult:
        """Execute web search"""
        start_time = datetime.now()
        query = args.get("query", "")
        num_results = min(args.get("num_results", 5), 10)
        
        # Mock results for demo (in production, use SerpAPI)
        mock_results = [
            {
                "title": f"Result about {query}",
                "link": f"https://example.com/article_{i}",
                "snippet": f"Information about {query} result {i+1}"
            }
            for i in range(num_results)
        ]
        
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        
        return MCPToolResult(
            tool_name="search_web",
            status="success",
            result={"results": mock_results},
            execution_time_ms=elapsed
        )
    
    def _search_news(self, args: Dict[str, Any]) -> MCPToolResult:
        """Execute news search"""
        start_time = datetime.now()
        query = args.get("query", "")
        
        mock_articles = [
            {
                "title": f"News: {query}",
                "source": "NewsAPI",
                "date": "2024-01-15",
                "content": f"Article about {query}"
            }
        ]
        
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        
        return MCPToolResult(
            tool_name="search_news",
            status="success",
            result={"articles": mock_articles},
            execution_time_ms=elapsed
        )


class DatabaseMCPServer(MCPServer):
    """MCP Server for database queries"""
    
    def __init__(self, connection_string: Optional[str] = None):
        super().__init__("database_mcp", "database")
        self.connection_string = connection_string or "sqlite:///food_rescue.db"
        self._define_tools()
    
    def _define_tools(self):
        """Define available database tools"""
        self.tools["query_recipients"] = MCPToolDefinition(
            tool_name="query_recipients",
            tool_type="database",
            mcp_server="database_mcp",
            description="Query recipient database",
            input_schema={
                "type": "object",
                "properties": {
                    "filters": {"type": "object", "description": "Query filters"}
                },
                "required": ["filters"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "recipients": {"type": "array"}
                }
            }
        )
        
        self.tools["query_donors"] = MCPToolDefinition(
            tool_name="query_donors",
            tool_type="database",
            mcp_server="database_mcp",
            description="Query donor database",
            input_schema={
                "type": "object",
                "properties": {
                    "donor_id": {"type": "string"}
                }
            },
            output_schema={
                "type": "object",
                "properties": {
                    "donor": {"type": "object"}
                }
            }
        )
        
        self.tools["get_statistics"] = MCPToolDefinition(
            tool_name="get_statistics",
            tool_type="database",
            mcp_server="database_mcp",
            description="Get database statistics",
            input_schema={
                "type": "object",
                "properties": {
                    "metric": {"type": "string"}
                }
            },
            output_schema={
                "type": "object",
                "properties": {
                    "stat": {"type": "number"}
                }
            }
        )
    
    def connect(self) -> bool:
        """Connect to database"""
        try:
            print(f"✓ Connecting to {self.server_name}...")
            self.connected = True
            print(f"✓ Connected to database: {self.connection_string}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from database"""
        self.connected = False
        print(f"✓ Disconnected from {self.server_name}")
        return True
    
    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> MCPToolResult:
        """Execute database tool"""
        start_time = datetime.now()
        
        try:
            if not self.connected:
                raise ConnectionError("Not connected to database")
            
            if tool_name == "query_recipients":
                return self._query_recipients(args)
            elif tool_name == "query_donors":
                return self._query_donors(args)
            elif tool_name == "get_statistics":
                return self._get_statistics(args)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        
        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            return MCPToolResult(
                tool_name=tool_name,
                status="error",
                result={},
                execution_time_ms=elapsed,
                error_message=str(e)
            )
    
    def _query_recipients(self, args: Dict[str, Any]) -> MCPToolResult:
        """Query recipients from database"""
        start_time = datetime.now()
        
        # Mock recipients for demo
        mock_recipients = [
            {
                "id": "r1",
                "name": "Community Kitchen",
                "location": "Downtown",
                "capacity": 100,
                "food_preference": ["cooked_veg", "rice"]
            },
            {
                "id": "r2",
                "name": "Shelter A",
                "location": "North",
                "capacity": 150,
                "food_preference": ["all"]
            }
        ]
        
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        
        return MCPToolResult(
            tool_name="query_recipients",
            status="success",
            result={"recipients": mock_recipients},
            execution_time_ms=elapsed
        )
    
    def _query_donors(self, args: Dict[str, Any]) -> MCPToolResult:
        """Query donor from database"""
        start_time = datetime.now()
        donor_id = args.get("donor_id", "d1")
        
        mock_donor = {
            "id": donor_id,
            "name": "Main Cafeteria",
            "location": "Campus Center"
        }
        
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        
        return MCPToolResult(
            tool_name="query_donors",
            status="success",
            result={"donor": mock_donor},
            execution_time_ms=elapsed
        )
    
    def _get_statistics(self, args: Dict[str, Any]) -> MCPToolResult:
        """Get statistics from database"""
        start_time = datetime.now()
        metric = args.get("metric", "total_redistributed")
        
        stats = {
            "total_redistributed": 5234,
            "active_recipients": 47,
            "total_donors": 12
        }
        
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        
        return MCPToolResult(
            tool_name="get_statistics",
            status="success",
            result={"stat": stats.get(metric, 0)},
            execution_time_ms=elapsed
        )


class FileParserMCPServer(MCPServer):
    """MCP Server for file parsing"""
    
    def __init__(self):
        super().__init__("file_parser_mcp", "file_parser")
        self._define_tools()
    
    def _define_tools(self):
        """Define available file tools"""
        self.tools["parse_csv"] = MCPToolDefinition(
            tool_name="parse_csv",
            tool_type="file_parser",
            mcp_server="file_parser_mcp",
            description="Parse CSV files",
            input_schema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "delimiter": {"type": "string"}
                },
                "required": ["file_path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "rows": {"type": "array"}
                }
            }
        )
        
        self.tools["parse_json"] = MCPToolDefinition(
            tool_name="parse_json",
            tool_type="file_parser",
            mcp_server="file_parser_mcp",
            description="Parse JSON files",
            input_schema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "data": {"type": "object"}
                }
            }
        )
    
    def connect(self) -> bool:
        """Connect to file parser"""
        try:
            print(f"✓ Connecting to {self.server_name}...")
            self.connected = True
            print(f"✓ File parser ready")
            return True
        except Exception as e:
            print(f"✗ Failed to connect: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from file parser"""
        self.connected = False
        print(f"✓ Disconnected from {self.server_name}")
        return True
    
    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> MCPToolResult:
        """Execute file parser tool"""
        start_time = datetime.now()
        
        try:
            if not self.connected:
                raise ConnectionError("Not connected to file parser")
            
            if tool_name == "parse_csv":
                return self._parse_csv(args)
            elif tool_name == "parse_json":
                return self._parse_json(args)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        
        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds() * 1000
            return MCPToolResult(
                tool_name=tool_name,
                status="error",
                result={},
                execution_time_ms=elapsed,
                error_message=str(e)
            )
    
    def _parse_csv(self, args: Dict[str, Any]) -> MCPToolResult:
        """Parse CSV file"""
        start_time = datetime.now()
        file_path = args.get("file_path", "")
        
        # Mock CSV parsing
        mock_rows = [
            {"id": "r1", "name": "Recipient 1"},
            {"id": "r2", "name": "Recipient 2"}
        ]
        
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        
        return MCPToolResult(
            tool_name="parse_csv",
            status="success",
            result={"rows": mock_rows},
            execution_time_ms=elapsed
        )
    
    def _parse_json(self, args: Dict[str, Any]) -> MCPToolResult:
        """Parse JSON file"""
        start_time = datetime.now()
        
        mock_data = {
            "version": "1.0",
            "records": []
        }
        
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        
        return MCPToolResult(
            tool_name="parse_json",
            status="success",
            result={"data": mock_data},
            execution_time_ms=elapsed
        )


class MCPManager:
    """Central manager for all MCP servers"""
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
        self.connected_servers: List[str] = []
        self.execution_log: List[Dict[str, Any]] = []
    
    def register_server(self, server: MCPServer):
        """Register an MCP server"""
        self.servers[server.server_name] = server
        print(f"✓ Registered MCP server: {server.server_name}")
    
    def connect_all(self) -> bool:
        """Connect to all registered servers"""
        print("\n" + "=" * 70)
        print("CONNECTING TO MCP SERVERS")
        print("=" * 70)
        
        all_connected = True
        for server_name, server in self.servers.items():
            if server.connect():
                self.connected_servers.append(server_name)
            else:
                all_connected = False
        
        print(f"\n✓ Connected to {len(self.connected_servers)}/{len(self.servers)} servers")
        return all_connected
    
    def disconnect_all(self) -> bool:
        """Disconnect from all servers"""
        for server_name in list(self.connected_servers):
            self.servers[server_name].disconnect()
            self.connected_servers.remove(server_name)
        return True
    
    def execute_tool(self, server_name: str, tool_name: str, 
                    args: Dict[str, Any]) -> MCPToolResult:
        """Execute a tool on a specific server"""
        if server_name not in self.servers:
            return MCPToolResult(
                tool_name=tool_name,
                status="error",
                result={},
                execution_time_ms=0,
                error_message=f"Server {server_name} not found"
            )
        
        server = self.servers[server_name]
        result = server.execute_tool(tool_name, args)
        
        # Log execution
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "server": server_name,
            "tool": tool_name,
            "status": result.status,
            "execution_time_ms": result.execution_time_ms
        })
        
        return result
    
    def list_available_tools(self) -> Dict[str, List[MCPToolDefinition]]:
        """List all available tools across servers"""
        tools = {}
        for server_name, server in self.servers.items():
            tools[server_name] = server.list_tools()
        return tools
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get statistics about tool executions"""
        if not self.execution_log:
            return {"total_executions": 0}
        
        total_time = sum(e["execution_time_ms"] for e in self.execution_log)
        successful = sum(1 for e in self.execution_log if e["status"] == "success")
        
        return {
            "total_executions": len(self.execution_log),
            "successful": successful,
            "failed": len(self.execution_log) - successful,
            "total_time_ms": total_time,
            "average_time_ms": total_time / len(self.execution_log)
        }


# Global MCP manager
mcp_manager = MCPManager()


def initialize_mcp():
    """Initialize all MCP servers"""
    # Register servers
    mcp_manager.register_server(WebSearchMCPServer())
    mcp_manager.register_server(DatabaseMCPServer())
    mcp_manager.register_server(FileParserMCPServer())
    
    # Connect all
    mcp_manager.connect_all()


if __name__ == "__main__":
    # Example usage
    print("\n" + "=" * 70)
    print("MCP INTEGRATION DEMO")
    print("=" * 70)
    
    # Initialize MCP
    initialize_mcp()
    
    # List available tools
    print("\n[1] Available MCP Tools:")
    all_tools = mcp_manager.list_available_tools()
    for server, tools in all_tools.items():
        print(f"\n  {server}:")
        for tool in tools:
            print(f"    - {tool.tool_name}: {tool.description}")
    
    # Execute sample tools
    print("\n[2] Executing Sample Tools:")
    
    # Web search
    print("\n  → Web Search:")
    result = mcp_manager.execute_tool(
        "web_search_mcp",
        "search_web",
        {"query": "food safety guidelines"}
    )
    print(f"    Status: {result.status}, Time: {result.execution_time_ms:.2f}ms")
    
    # Database query
    print("\n  → Database Query:")
    result = mcp_manager.execute_tool(
        "database_mcp",
        "query_recipients",
        {"filters": {}}
    )
    print(f"    Status: {result.status}, Time: {result.execution_time_ms:.2f}ms")
    
    # File parsing
    print("\n  → File Parser:")
    result = mcp_manager.execute_tool(
        "file_parser_mcp",
        "parse_csv",
        {"file_path": "recipients.csv"}
    )
    print(f"    Status: {result.status}, Time: {result.execution_time_ms:.2f}ms")
    
    # Statistics
    print("\n[3] Execution Statistics:")
    stats = mcp_manager.get_execution_stats()
    print(f"  Total executions: {stats['total_executions']}")
    print(f"  Successful: {stats['successful']}")
    print(f"  Average time: {stats['average_time_ms']:.2f}ms")
    
    # Cleanup
    mcp_manager.disconnect_all()
    print("\n✓ MCP demo complete")
