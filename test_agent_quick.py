#!/usr/bin/env python3
"""Quick test to verify agent code works"""

import sys
import ast

def test_syntax():
    """Test that auto_pr_scanner.py has valid syntax"""
    print("Testing auto_pr_scanner.py syntax...")
    
    with open('auto_pr_scanner.py', 'r') as f:
        code = f.read()
    
    try:
        ast.parse(code)
        print("✅ Syntax is valid!")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

def test_imports():
    """Test that imports work"""
    print("\nTesting imports...")
    
    try:
        import asyncio
        from openai import OpenAI
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        import requests
        from dotenv import load_dotenv
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_class_structure():
    """Test that the class can be instantiated"""
    print("\nTesting class structure...")
    
    try:
        # Import the module
        sys.path.insert(0, '.')
        from auto_pr_scanner import AutoPRScanner
        
        # Try to create instance (won't connect MCPs yet)
        scanner = AutoPRScanner("test-owner", "test-repo")
        
        print("✅ Class structure is valid!")
        print(f"   - Model: {scanner.model}")
        print(f"   - Repo: {scanner.repo_owner}/{scanner.repo_name}")
        return True
    except Exception as e:
        print(f"❌ Class error: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("  QUICK AGENT TEST")
    print("="*60 + "\n")
    
    results = []
    results.append(("Syntax", test_syntax()))
    results.append(("Imports", test_imports()))
    results.append(("Class", test_class_structure()))
    
    print("\n" + "="*60)
    print("  RESULTS")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:15} {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! Agent is ready to run!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        sys.exit(1)
