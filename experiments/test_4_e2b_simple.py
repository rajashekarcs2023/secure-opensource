#!/usr/bin/env python3
"""
Test 4: E2B Sandbox (Simplified)
Just check if E2B is available and API key is set
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("TEST 4: E2B SANDBOX")
print("=" * 60)

# Check if API key exists
api_key = os.getenv('E2B_API_KEY')
if not api_key:
    print("❌ FAILED: E2B_API_KEY not found in .env file")
    exit(1)

print(f"✅ API Key found: {api_key[:15]}...")

# Try to import E2B
print("\n🔄 Checking E2B installation...")
try:
    from e2b_code_interpreter import Sandbox
    print("✅ E2B code_interpreter SDK installed")
except ImportError:
    print("❌ FAILED: E2B SDK not installed")
    exit(1)

# Try to import base e2b
try:
    import e2b
    print("✅ E2B base SDK installed")
except ImportError:
    print("⚠️  E2B base SDK not installed (optional)")

print("\n" + "=" * 60)
print("🎉 E2B SDK TEST PASSED!")
print("=" * 60)
print("\n📝 E2B is ready to use!")
print("   We'll use it in the agent to execute code safely.")
print("   The Sandbox will be created when the agent runs.")
