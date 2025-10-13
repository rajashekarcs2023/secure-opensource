#!/usr/bin/env python3
"""
Test E2B MCP Server connection
"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()

async def test_e2b():
    print("🧪 Testing E2B MCP Server\n")
    
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@e2b/mcp-server"],
        env={"E2B_API_KEY": os.getenv("E2B_API_KEY")}
    )
    
    print("🔌 Connecting to E2B MCP...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("✅ Connected!\n")
            
            # List available tools
            print("📋 Available tools:")
            response = await session.list_tools()
            for tool in response.tools:
                print(f"   - {tool.name}")
            
            print("\n🎯 Testing code execution...")
            
            # Try to execute simple code
            try:
                result = await session.call_tool(
                    "run_code",
                    {
                        "code": "print('Hello from E2B!')\nresult = 2 + 2\nprint(f'2 + 2 = {result}')"
                    }
                )
                print(f"✅ Code executed!")
                print(f"Result: {result.content}\n")
            except Exception as e:
                print(f"❌ Execution failed: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_e2b())
