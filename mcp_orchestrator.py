"""
MCP Orchestrator - Connects to all MCP servers
Manages communication between agent and multiple MCP servers
"""

import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()

class MCPOrchestrator:
    """Orchestrates multiple MCP server connections"""
    
    def __init__(self):
        self.sessions = {}
        self.clients = {}
    
    async def connect_e2b(self):
        """Connect to E2B MCP server"""
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@e2b/mcp-server"],
            env={
                "E2B_API_KEY": os.getenv("E2B_API_KEY")
            }
        )
        
        read, write = await stdio_client(server_params).__aenter__()
        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()
        
        self.clients['e2b'] = (read, write)
        self.sessions['e2b'] = session
        print("✅ Connected to E2B MCP server")
        return session
    
    async def connect_deepresearch(self):
        """Connect to Octagon DeepResearch MCP server"""
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "octagon-deep-research-mcp"],
            env={
                "OCTAGON_API_KEY": os.getenv("OCTAGON_API_KEY")
            }
        )
        
        read, write = await stdio_client(server_params).__aenter__()
        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()
        
        self.clients['deepresearch'] = (read, write)
        self.sessions['deepresearch'] = session
        print("✅ Connected to DeepResearch MCP server")
        return session
    
    async def connect_debuggai(self):
        """Connect to DebuggAI MCP server"""
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@debugg-ai/debugg-ai-mcp"],
            env={
                "DEBUGGAI_API_KEY": os.getenv("DEBUGGAI_API_KEY"),
                "DEBUGGAI_LOCAL_PORT": "3000"
            }
        )
        
        read, write = await stdio_client(server_params).__aenter__()
        session = ClientSession(read, write)
        await session.__aenter__()
        await session.initialize()
        
        self.clients['debuggai'] = (read, write)
        self.sessions['debuggai'] = session
        print("✅ Connected to DebuggAI MCP server")
        return session
    
    async def connect_all(self):
        """Connect to all MCP servers"""
        print("🔌 Connecting to MCP servers...")
        
        try:
            await self.connect_e2b()
        except Exception as e:
            print(f"⚠️  E2B connection failed: {e}")
        
        try:
            await self.connect_deepresearch()
        except Exception as e:
            print(f"⚠️  DeepResearch connection failed: {e}")
        
        try:
            await self.connect_debuggai()
        except Exception as e:
            print(f"⚠️  DebuggAI connection failed: {e}")
        
        print(f"✅ Connected to {len(self.sessions)} MCP servers\n")
    
    async def call_tool(self, server_name, tool_name, arguments):
        """Call a tool on a specific MCP server"""
        if server_name not in self.sessions:
            raise ValueError(f"Not connected to {server_name}")
        
        session = self.sessions[server_name]
        result = await session.call_tool(tool_name, arguments)
        return result
    
    async def list_tools(self, server_name):
        """List available tools from a server"""
        if server_name not in self.sessions:
            raise ValueError(f"Not connected to {server_name}")
        
        session = self.sessions[server_name]
        tools = await session.list_tools()
        return tools
    
    async def disconnect_all(self):
        """Disconnect from all MCP servers"""
        for name, session in self.sessions.items():
            try:
                await session.__aexit__(None, None, None)
                print(f"✅ Disconnected from {name}")
            except Exception as e:
                print(f"⚠️  Error disconnecting from {name}: {e}")
        
        for name, (read, write) in self.clients.items():
            try:
                await read.__aexit__(None, None, None)
                await write.__aexit__(None, None, None)
            except Exception as e:
                pass
        
        self.sessions.clear()
        self.clients.clear()

# Test the orchestrator
async def test_orchestrator():
    """Test MCP connections"""
    orchestrator = MCPOrchestrator()
    
    try:
        await orchestrator.connect_all()
        
        # List available tools from each server
        for server_name in orchestrator.sessions.keys():
            print(f"\n📋 Tools from {server_name}:")
            tools = await orchestrator.list_tools(server_name)
            for tool in tools.tools[:3]:  # Show first 3 tools
                print(f"   - {tool.name}: {tool.description[:60]}...")
        
    finally:
        await orchestrator.disconnect_all()

if __name__ == "__main__":
    print("🧪 Testing MCP Orchestrator\n")
    asyncio.run(test_orchestrator())
