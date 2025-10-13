#!/usr/bin/env python3
"""
Test 3: Cycode CLI
Test Cycode installation and authentication
"""

import subprocess
import sys

print("=" * 60)
print("TEST 3: CYCODE CLI")
print("=" * 60)

# Test 1: Check if Cycode is installed
print("\n🔄 Checking Cycode installation...")
try:
    result = subprocess.run(['cycode', '--version'], 
                          capture_output=True, 
                          text=True, 
                          timeout=5)
    
    if result.returncode == 0:
        version = result.stdout.strip()
        print(f"✅ Cycode installed: {version}")
    else:
        print("❌ Cycode not responding properly")
        exit(1)
        
except FileNotFoundError:
    print("❌ FAILED: Cycode not installed")
    print("\nInstall with:")
    print("  pip3 install cycode")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test 2: Check authentication
print("\n🔄 Checking Cycode authentication...")
try:
    result = subprocess.run(['cycode', 'status'], 
                          capture_output=True, 
                          text=True, 
                          timeout=10)
    
    if result.returncode == 0:
        print("✅ Cycode authenticated")
        print(f"   Status: {result.stdout.strip()}")
    else:
        print("❌ Not authenticated")
        print("\nAuthenticate with:")
        print("  cycode auth")
        print("\nOr configure manually:")
        print("  cycode configure")
        exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test 3: Check MCP support (requires Python 3.10+)
print("\n🔄 Checking MCP server support...")
py_version = sys.version_info

if py_version.major == 3 and py_version.minor >= 10:
    print(f"✅ Python {py_version.major}.{py_version.minor} - MCP supported")
    
    try:
        result = subprocess.run(['cycode', 'mcp', '--help'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        
        if 'Start the Model Context Protocol' in result.stdout or result.returncode == 0:
            print("✅ Cycode MCP server available")
        else:
            print("⚠️  MCP command not found")
    except Exception as e:
        print(f"⚠️  MCP check failed: {e}")
else:
    print(f"⚠️  Python {py_version.major}.{py_version.minor} - MCP requires 3.10+")
    print("   (Cycode still works, but MCP server won't be available)")

# Test 4: Check scan types available
print("\n🔄 Checking available scan types...")
try:
    result = subprocess.run(['cycode', 'scan', '--help'], 
                          capture_output=True, 
                          text=True, 
                          timeout=5)
    
    scan_types = []
    if 'secret' in result.stdout.lower():
        scan_types.append('Secrets')
    if 'sca' in result.stdout.lower():
        scan_types.append('SCA')
    if 'sast' in result.stdout.lower():
        scan_types.append('SAST')
    if 'iac' in result.stdout.lower():
        scan_types.append('IaC')
    
    if scan_types:
        print(f"✅ Available scans: {', '.join(scan_types)}")
    else:
        print("⚠️  Couldn't determine scan types")
        
except Exception as e:
    print(f"⚠️  Scan check failed: {e}")

print("\n" + "=" * 60)
print("🎉 CYCODE CLI TEST PASSED!")
print("=" * 60)
print("\n📝 Next step: Test Cycode MCP server")
print("   Run in one terminal: cycode mcp")
print("   (Keep it running while agent works)")
