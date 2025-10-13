#!/usr/bin/env python3
"""
Test 4: E2B Sandbox
Test E2B code execution sandbox
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
    print("\nHow to get an E2B API key:")
    print("1. Go to: https://e2b.dev/")
    print("2. Sign up (free tier: 100 sandbox hours/month)")
    print("3. Go to: https://e2b.dev/dashboard")
    print("4. Click 'API Keys' → 'Create new API key'")
    print("5. Copy key and add to .env as: E2B_API_KEY=e2b_xxx")
    exit(1)

print(f"✅ API Key found: {api_key[:15]}...")

# Try to import E2B
print("\n🔄 Checking E2B installation...")
try:
    from e2b_code_interpreter import Sandbox
    print("✅ E2B SDK installed")
except ImportError:
    print("❌ FAILED: E2B SDK not installed")
    print("\nInstall with:")
    print("  pip3 install e2b-code-interpreter")
    exit(1)

# Test sandbox creation
print("\n🔄 Creating sandbox...")
try:
    # Set API key in environment
    os.environ['E2B_API_KEY'] = api_key
    sandbox = Sandbox()
    print("✅ Sandbox created successfully")
    
    # Test 1: Simple Python execution
    print("\n🔄 Test 1: Running Python code...")
    execution = sandbox.run_code("print('Hello from E2B sandbox!')")
    
    if execution.results:
        result = execution.results[0]
        print(f"✅ Code executed successfully")
        print(f"   Output: {result.text}")
    else:
        print("⚠️  Code ran but no output")
    
    # Test 2: Math calculation
    print("\n🔄 Test 2: Math calculation...")
    execution = sandbox.run_code("result = 15 + 27\nprint(f'15 + 27 = {result}')")
    
    if execution.results:
        result = execution.results[0]
        print(f"✅ Calculation successful")
        print(f"   Output: {result.text}")
    
    # Test 3: File system access
    print("\n🔄 Test 3: File system access...")
    execution = sandbox.run_code("""
import os
print(f"Current directory: {os.getcwd()}")
print(f"Files: {os.listdir('.')[:5]}")
""")
    
    if execution.results:
        result = execution.results[0]
        print(f"✅ File system accessible")
        print(f"   Output: {result.text[:100]}...")
    
    # Test 4: Error handling
    print("\n🔄 Test 4: Error handling...")
    execution = sandbox.run_code("1 / 0  # This should error")
    
    if execution.error:
        print(f"✅ Error handling works")
        print(f"   Error: {execution.error.name}: {execution.error.value[:50]}...")
    
    # Close sandbox
    sandbox.close()
    print("\n✅ Sandbox closed properly")
    
    print("\n" + "=" * 60)
    print("🎉 E2B SANDBOX TEST PASSED!")
    print("=" * 60)
    print("\n📝 E2B can:")
    print("   - Execute Python code securely")
    print("   - Access file system")
    print("   - Handle errors gracefully")
    print("   - Perfect for reproducing vulnerabilities!")
    
except Exception as e:
    print(f"\n❌ FAILED: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check API key is correct")
    print("2. Verify internet connection")
    print("3. Check E2B service status: https://status.e2b.dev/")
    exit(1)
