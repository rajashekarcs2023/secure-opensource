#!/usr/bin/env python3
"""Test Perplexity MCP directly"""

import os
import asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

async def test_perplexity():
    print("Testing Perplexity MCP...")
    
    params = StdioServerParameters(
        command="npx",
        args=["-y", "@perplexity-ai/mcp-server"],
        env={"PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY")}
    )
    
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("✅ Perplexity MCP connected!")
            
            # List available tools
            tools = await session.list_tools()
            print(f"\n📋 Available tools: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"   • {tool.name}")
            
            # Test 1: Simple ask
            print("\n[TEST 1] Testing perplexity_ask...")
            try:
                result = await asyncio.wait_for(
                    session.call_tool(
                        "perplexity_ask",
                        {
                            "messages": [
                                {"role": "user", "content": "What is SQL Injection?"}
                            ]
                        }
                    ),
                    timeout=10.0
                )
                print(f"✅ Response: {str(result.content[0].text)[:200]}...")
            except asyncio.TimeoutError:
                print("❌ Timeout after 10 seconds")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 2: Search (if available)
            print("\n[TEST 2] Testing perplexity_search...")
            try:
                result = await asyncio.wait_for(
                    session.call_tool(
                        "perplexity_search",
                        {"query": "SQL Injection CVSS score"}
                    ),
                    timeout=10.0
                )
                print(f"✅ Response: {str(result.content[0].text)[:200]}...")
            except asyncio.TimeoutError:
                print("❌ Timeout after 10 seconds")
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_perplexity())
