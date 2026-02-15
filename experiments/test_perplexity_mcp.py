#!/usr/bin/env python3
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()

async def test_perplexity():
    print("🧪 Testing Perplexity MCP\n")
    
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@perplexity-ai/mcp-server"],
        env={"PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY")}
    )
    
    print("🔌 Connecting...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Connected!\n")
            
            response = await session.list_tools()
            print("📋 Tools:")
            for tool in response.tools:
                print(f"   - {tool.name}")
            
            print("\n🎯 Testing search...")
            result = await session.call_tool(
                "perplexity_search",
                {"query": "SQL injection CVE 2024"}
            )
            print(f"✅ Search works! {str(result.content)[:100]}...\n")

if __name__ == "__main__":
    asyncio.run(test_perplexity())
