#!/usr/bin/env python3
"""
Test 1: NVIDIA Nemotron API
Simple test to verify NVIDIA API is working
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print("=" * 60)
print("TEST 1: NVIDIA NEMOTRON API")
print("=" * 60)

# Check if API key exists
api_key = os.getenv("NVIDIA_API_KEY")
if not api_key:
    print("❌ FAILED: NVIDIA_API_KEY not found in .env file")
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...")

# Try to connect
try:
    print("\n🔄 Connecting to NVIDIA API...")
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    
    print("🔄 Sending test request...")
    completion = client.chat.completions.create(
        model="nvidia/nvidia-nemotron-nano-9b-v2",
        messages=[{"role": "user", "content": "Say 'Hello! I am working correctly.' if you can read this."}],
        max_tokens=50,
        temperature=0.5
    )
    
    response = completion.choices[0].message.content
    print(f"\n✅ SUCCESS! Got response:")
    print(f"   {response}")
    
    # Test reasoning capabilities (with thinking tokens)
    print("\n🔄 Testing reasoning capabilities...")
    completion = client.chat.completions.create(
        model="nvidia/nvidia-nemotron-nano-9b-v2",
        messages=[{"role": "user", "content": "What is 15 + 27?"}],
        temperature=0.6,
        max_tokens=100,
        extra_body={
            "min_thinking_tokens": 50,
            "max_thinking_tokens": 100
        }
    )
    
    reasoning = getattr(completion.choices[0].message, "reasoning_content", None)
    response = completion.choices[0].message.content
    
    if reasoning:
        print(f"\n✅ Reasoning mode working!")
        print(f"   Reasoning: {reasoning[:100]}...")
    
    print(f"   Answer: {response}")
    
    print("\n" + "=" * 60)
    print("🎉 NVIDIA API TEST PASSED!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ FAILED: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check your API key is correct")
    print("2. Verify internet connection")
    print("3. Try regenerating API key at: https://build.nvidia.com")
    exit(1)
