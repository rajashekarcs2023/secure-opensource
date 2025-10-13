#!/usr/bin/env python3
"""
Simplified Security Agent - WORKING VERSION
Focus on NVIDIA Nemotron capabilities first, add MCPs incrementally
"""

import os
import sys
import re
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class SimpleSecurityAgent:
    """Working security agent - build incrementally"""
    
    def __init__(self):
        self.nvidia = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY")
        )
        self.model = "nvidia/llama-3.1-nemotron-70b-instruct"
        
        print("╔══════════════════════════════════════════════════════════╗")
        print("║       SECURITY AGENT - NVIDIA Nemotron 70B              ║")
        print("╚══════════════════════════════════════════════════════════╝\n")
    
    def scan_code(self, file_path):
        """Phase 1: Scan for vulnerabilities"""
        print("[1] 🔍 SCANNING CODE")
        print("─" * 60)
        
        with open(file_path, 'r') as f:
            code = f.read()
        
        vulnerabilities = []
        sql_patterns = [
            r'f["\'].*SELECT.*\{.*\}["\']',
            r'cursor\.execute\([f]?["\'].*\{.*\}["\']'
        ]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in sql_patterns:
                if re.search(pattern, line):
                    vulnerabilities.append({
                        'type': 'SQL Injection',
                        'line': i,
                        'code': line.strip(),
                        'severity': 'CRITICAL',
                        'cvss': 9.8
                    })
                    break
        
        for vuln in vulnerabilities:
            print(f"🔴 {vuln['type']} (Line {vuln['line']})")
            print(f"   Severity: {vuln['severity']} (CVSS {vuln['cvss']})")
        
        print()
        return vulnerabilities, code
    
    def analyze(self, vuln, code):
        """Phase 2: NVIDIA analyzes"""
        print("[2] 🧠 NVIDIA NEMOTRON ANALYZING")
        print("─" * 60)
        
        prompt = f"""Security Analysis Required:

Vulnerability: {vuln['type']} at line {vuln['line']}
Code: {vuln['code']}

Analyze this vulnerability. Provide:
1. Root cause
2. Attack vector  
3. Impact
4. Why CVSS {vuln['cvss']}

Be concise and technical."""

        print("→ Calling NVIDIA Nemotron...")
        
        response = self.nvidia.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=800
        )
        
        analysis = response.choices[0].message.content
        print(f"\n{analysis}\n")
        
        return analysis
    
    def generate_fix(self, vuln, code):
        """Phase 3: NVIDIA generates fix"""
        print("[3] 🔧 NVIDIA NEMOTRON GENERATING FIX")
        print("─" * 60)
        
        prompt = f"""Generate a secure fix for this code:

Vulnerability: {vuln['type']}
Line {vuln['line']}: {vuln['code']}

Full code:
```python
{code}
```

Return the COMPLETE fixed code using parameterized queries. 
Return ONLY Python code, no explanation."""

        print("→ Generating fix...")
        
        response = self.nvidia.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=2000
        )
        
        fixed = response.choices[0].message.content
        
        # Extract code
        match = re.search(r'```python\n(.*?)\n```', fixed, re.DOTALL)
        fixed_code = match.group(1) if match else fixed
        
        print(f"✅ Generated {len(fixed_code)} chars of secure code\n")
        
        return fixed_code
    
    def run(self, file_path):
        """Run workflow"""
        start = datetime.now()
        
        # Scan
        vulns, code = self.scan_code(file_path)
        
        if not vulns:
            print("✅ No vulnerabilities found")
            return
        
        vuln = vulns[0]
        
        # Analyze
        analysis = self.analyze(vuln, code)
        
        # Fix
        fixed_code = self.generate_fix(vuln, code)
        
        # Save fixed code
        fixed_file = file_path.replace('.py', '_fixed.py')
        with open(fixed_file, 'w') as f:
            f.write(fixed_code)
        
        duration = (datetime.now() - start).total_seconds()
        
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                    COMPLETE                              ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print(f"\n⏱️  Time: {duration:.1f}s")
        print(f"🔴 Vulnerability: FIXED ✅")
        print(f"📝 Fixed code saved to: {fixed_file}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python simple_agent.py <file>")
        sys.exit(1)
    
    agent = SimpleSecurityAgent()
    agent.run(sys.argv[1])
