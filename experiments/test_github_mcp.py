#!/usr/bin/env python3
"""Test GitHub MCP connection"""

import os
import asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

async def test_github_mcp():
    print("Testing GitHub MCP...")
    
    params = StdioServerParameters(
        command="docker",
        args=[
            "run", "-i", "--rm",
            "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
            "ghcr.io/github/github-mcp-server"
        ],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")}
    )
    
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("✅ GitHub MCP connected!")
            
            # List available tools
            tools = await session.list_tools()
            print(f"\n📋 Available tools: {len(tools.tools)}")
            for tool in tools.tools[:10]:
                print(f"   • {tool.name}")
            
            print("\n✅ GitHub MCP is working!")

if __name__ == "__main__":
    asyncio.run(test_github_mcp())
