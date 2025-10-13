#!/usr/bin/env python3
"""
Test All MCP Servers for NVIDIA Hackathon
Tests each component before building the main agent
"""

import os
import sys
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_test(name, status, message=""):
    icon = f"{Colors.GREEN}✅" if status else f"{Colors.RED}❌"
    print(f"{icon} {Colors.BOLD}{name}{Colors.RESET}")
    if message:
        print(f"   {message}")
    print(Colors.RESET)

def test_nvidia_api():
    """Test NVIDIA Nemotron API"""
    print_header("Testing NVIDIA Nemotron API")
    
    try:
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            print_test("NVIDIA API Key", False, "API key not found in .env")
            return False
        
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        
        # Simple test request
        completion = client.chat.completions.create(
            model="nvidia/nvidia-nemotron-nano-9b-v2",
            messages=[{"role": "user", "content": "Say 'test successful' if you can read this."}],
            max_tokens=50,
            temperature=0.5
        )
        
        response = completion.choices[0].message.content
        print_test("NVIDIA Nemotron API", True, f"Response: {response[:50]}...")
        return True
        
    except Exception as e:
        print_test("NVIDIA Nemotron API", False, f"Error: {str(e)}")
        return False

def test_github_api():
    """Test GitHub API access"""
    print_header("Testing GitHub API")
    
    try:
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            print_test("GitHub Token", False, "GITHUB_TOKEN not found in .env")
            return False
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Test authentication
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user = response.json()
            print_test("GitHub API", True, f"Authenticated as: {user['login']}")
            
            # Test repo access
            repos_response = requests.get('https://api.github.com/user/repos', headers=headers)
            if repos_response.status_code == 200:
                print_test("GitHub Repos Access", True, f"Can access repositories")
            return True
        else:
            print_test("GitHub API", False, f"Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test("GitHub API", False, f"Error: {str(e)}")
        return False

def test_e2b_api():
    """Test E2B Sandbox API"""
    print_header("Testing E2B Sandbox API")
    
    try:
        api_key = os.getenv('E2B_API_KEY')
        if not api_key:
            print_test("E2B API Key", False, "E2B_API_KEY not found in .env - install with: pip3 install e2b")
            return False
        
        # Try to import E2B
        try:
            from e2b_code_interpreter import Sandbox
            
            # Create sandbox and test
            with Sandbox(api_key=api_key) as sandbox:
                execution = sandbox.run_code("print('E2B sandbox is working!')")
                if execution.results:
                    print_test("E2B Sandbox", True, f"Execution successful: {execution.results[0].text}")
                    return True
                else:
                    print_test("E2B Sandbox", True, "Sandbox created successfully")
                    return True
                    
        except ImportError:
            print_test("E2B Installation", False, "E2B not installed. Run: pip3 install e2b-code-interpreter")
            return False
            
    except Exception as e:
        print_test("E2B Sandbox", False, f"Error: {str(e)}")
        return False

def test_cycode_cli():
    """Test Cycode CLI installation"""
    print_header("Testing Cycode CLI")
    
    try:
        import subprocess
        
        # Check if cycode is installed
        result = subprocess.run(['cycode', 'status'], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print_test("Cycode CLI", True, "Cycode CLI installed and authenticated")
            
            # Check if MCP command is available
            help_result = subprocess.run(['cycode', 'mcp', '--help'], capture_output=True, text=True, timeout=5)
            if 'Start the Model Context Protocol' in help_result.stdout or help_result.returncode == 0:
                print_test("Cycode MCP", True, "MCP server available")
            else:
                print_test("Cycode MCP", False, "MCP command not available - need Python 3.10+")
            return True
        else:
            print_test("Cycode CLI", False, "Not authenticated. Run: cycode auth")
            return False
            
    except FileNotFoundError:
        print_test("Cycode CLI", False, "Not installed. Run: pip3 install cycode")
        return False
    except Exception as e:
        print_test("Cycode CLI", False, f"Error: {str(e)}")
        return False

def test_debuggai():
    """Test DebuggAI MCP availability"""
    print_header("Testing DebuggAI MCP")
    
    try:
        api_key = os.getenv('DEBUGGAI_API_KEY')
        if not api_key:
            print_test("DebuggAI API Key", False, "DEBUGGAI_API_KEY not found in .env")
            return False
        
        import subprocess
        
        # Check if package is available
        result = subprocess.run(
            ['npx', '@debugg-ai/debugg-ai-mcp', '--version'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 or '@debugg-ai/debugg-ai-mcp' in result.stdout:
            print_test("DebuggAI MCP", True, "Package available")
            return True
        else:
            print_test("DebuggAI MCP", False, "Package not found. Run: npm install -g @debugg-ai/debugg-ai-mcp")
            return False
            
    except Exception as e:
        print_test("DebuggAI MCP", False, f"Error: {str(e)}")
        return False

def test_deepresearch():
    """Test DeepResearch (Octagon) MCP availability"""
    print_header("Testing DeepResearch (Octagon) MCP")
    
    try:
        api_key = os.getenv('OCTAGON_API_KEY')
        if not api_key:
            print_test("Octagon API Key", False, "OCTAGON_API_KEY not found in .env")
            return False
        
        import subprocess
        
        # Check if package is available
        result = subprocess.run(
            ['npx', 'octagon-deep-research-mcp', '--version'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 or 'octagon-deep-research-mcp' in result.stdout:
            print_test("DeepResearch MCP", True, "Package available")
            return True
        else:
            print_test("DeepResearch MCP", False, "Package not found. Run: npm install -g octagon-deep-research-mcp")
            return False
            
    except Exception as e:
        print_test("DeepResearch MCP", False, f"Error: {str(e)}")
        return False

def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print_test("Python Version", True, f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_test("Python Version", False, f"Python {version.major}.{version.minor}.{version.micro} - Need 3.10+")
        return False

def check_node_version():
    """Check Node.js version"""
    print_header("Checking Node.js Version")
    
    try:
        import subprocess
        result = subprocess.run(['node', '-v'], capture_output=True, text=True)
        version = result.stdout.strip()
        
        # Extract version number
        version_num = int(version.replace('v', '').split('.')[0])
        
        if version_num >= 16:
            print_test("Node.js Version", True, f"Node {version}")
            return True
        else:
            print_test("Node.js Version", False, f"Node {version} - Need 16+")
            return False
            
    except Exception as e:
        print_test("Node.js Version", False, "Node.js not installed")
        return False

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║        NVIDIA HACKATHON - MCP SERVER TEST SUITE          ║")
    print("║                                                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(Colors.RESET)
    
    results = {}
    
    # System checks
    results['python'] = check_python_version()
    results['node'] = check_node_version()
    
    # API tests
    results['nvidia'] = test_nvidia_api()
    results['github'] = test_github_api()
    results['e2b'] = test_e2b_api()
    results['cycode'] = test_cycode_cli()
    results['debuggai'] = test_debuggai()
    results['deepresearch'] = test_deepresearch()
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.RESET}\n")
    
    for name, status in results.items():
        icon = f"{Colors.GREEN}✅" if status else f"{Colors.RED}❌"
        print(f"{icon} {name.upper()}{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}")
    if passed == total:
        print(f"{Colors.GREEN}🎉 ALL TESTS PASSED! Ready to build the agent! 🎉{Colors.RESET}")
        return 0
    elif passed >= 5:  # Minimum viable (NVIDIA, GitHub, Cycode, E2B, DeepResearch)
        print(f"{Colors.YELLOW}⚠️  MINIMUM REQUIREMENTS MET - Can proceed with caution{Colors.RESET}")
        print(f"{Colors.YELLOW}   Consider fixing failed tests for full functionality{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}❌ CRITICAL TESTS FAILED - Fix issues before proceeding{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Next steps:{Colors.RESET}")
        print(f"1. Check SETUP_GUIDE.md for installation instructions")
        print(f"2. Verify all API keys are in .env file")
        print(f"3. Run: pip3 install -r requirements.txt")
        return 1

if __name__ == "__main__":
    exit(main())
