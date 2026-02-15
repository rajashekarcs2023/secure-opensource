#!/usr/bin/env python3
"""Test Exa MCP for code search"""

import os
import asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

async def test_exa():
    print("Testing Exa MCP...")
    
    # Check if EXA_API_KEY exists
    exa_key = os.getenv("EXA_API_KEY")
    if not exa_key:
        print("❌ EXA_API_KEY not found in .env")
        print("\nTo use Exa MCP:")
        print("1. Get API key from https://exa.ai")
        print("2. Add to .env: EXA_API_KEY=your_key")
        return
    
    params = StdioServerParameters(
        command="npx",
        args=["-y", "exa-mcp-server"],
        env={"EXA_API_KEY": exa_key}
    )
    
    try:
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("✅ Exa MCP connected!")
                
                # List available tools
                tools = await session.list_tools()
                print(f"\n📋 Available tools: {len(tools.tools)}")
                for tool in tools.tools:
                    print(f"   • {tool.name}")
                
                # Test code context search
                print("\n[TEST 1] Getting code context for SQL injection fix...")
                try:
                    result = await asyncio.wait_for(
                        session.call_tool(
                            "get_code_context_exa",
                            {"query": "SQL injection parameterized queries Flask fix"}
                        ),
                        timeout=15.0
                    )
                    print(f"✅ Found examples: {str(result.content[0].text)[:300]}...")
                except asyncio.TimeoutError:
                    print("❌ Timeout after 15 seconds")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Test web search
                print("\n[TEST 2] Web search for CVE examples...")
                try:
                    result = await asyncio.wait_for(
                        session.call_tool(
                            "web_search_exa",
                            {"query": "SQL injection CVE 2024 examples"}
                        ),
                        timeout=15.0
                    )
                    print(f"✅ Found results: {str(result.content[0].text)[:300]}...")
                except asyncio.TimeoutError:
                    print("❌ Timeout after 15 seconds")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
    except Exception as e:
        print(f"❌ Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(test_exa())
