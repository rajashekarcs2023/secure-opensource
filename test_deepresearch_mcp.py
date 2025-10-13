#!/usr/bin/env python3
"""
Test DeepResearch MCP Server connection
"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()

async def test_deepresearch():
    print("🧪 Testing DeepResearch MCP Server\n")
    
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "octagon-deep-research-mcp"],
        env={"OCTAGON_API_KEY": os.getenv("OCTAGON_API_KEY")}
    )
    
    print("🔌 Connecting to DeepResearch MCP...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("✅ Connected!\n")
            
            # List available tools
            print("📋 Available tools:")
            response = await session.list_tools()
            for tool in response.tools:
                print(f"   - {tool.name}")
            
            print("\n🎯 Testing research query...")
            
            # Try to research
            try:
                result = await session.call_tool(
                    "octagon-deep-research-agent",
                    {
                        "prompt": "Find recent CVEs related to SQL injection vulnerabilities in Python"
                    }
                )
                print(f"✅ Research completed!")
                print(f"Result: {str(result.content)[:200]}...\n")
            except Exception as e:
                print(f"❌ Research failed: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_deepresearch())
