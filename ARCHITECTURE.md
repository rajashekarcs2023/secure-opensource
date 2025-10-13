# 🏗️ Security Triage Agent Architecture

## 🎯 Multi-MCP Orchestration with NVIDIA Nemotron Nano 9B

```
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │         GitHub Repository               │
                    │     (Open Pull Requests)                │
                    │                                         │
                    └────────────────┬────────────────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │      🤖 Auto PR Scanner Agent           │
                    │                                         │
                    └────────────────┬────────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
    │                 │   │                 │   │                 │
    │  GitHub MCP     │   │  Perplexity     │   │   Exa MCP       │
    │                 │   │     MCP         │   │  Code Search    │
    │  • Read PRs     │   │                 │   │                 │
    │  • Get Files    │   │  • CVE Research │   │  • Find GitHub  │
    │  • Post Reviews │   │  • CVSS Scores  │   │    Examples     │
    │  • Create PRs   │   │  • Security     │   │  • Real Fixes   │
    │                 │   │    Intel        │   │  • Best Practices│
    └────────┬────────┘   └────────┬────────┘   └────────┬────────┘
             │                     │                     │
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   │
                                   ▼
              ╔════════════════════════════════════════════╗
              ║                                            ║
              ║    🧠 NVIDIA NEMOTRON NANO 9B              ║
              ║         (Core Intelligence)                ║
              ║                                            ║
              ║  ┌──────────────────────────────────────┐ ║
              ║  │  1. Vulnerability Analysis           │ ║
              ║  │     • Pattern Detection              │ ║
              ║  │     • CVSS Scoring                   │ ║
              ║  │     • Risk Assessment                │ ║
              ║  └──────────────────────────────────────┘ ║
              ║                                            ║
              ║  ┌──────────────────────────────────────┐ ║
              ║  │  2. Context Integration              │ ║
              ║  │     • Perplexity CVE Data           │ ║
              ║  │     • Exa Code Examples             │ ║
              ║  │     • Security Best Practices       │ ║
              ║  └──────────────────────────────────────┘ ║
              ║                                            ║
              ║  ┌──────────────────────────────────────┐ ║
              ║  │  3. Secure Code Generation           │ ║
              ║  │     • Parameterized Queries          │ ║
              ║  │     • Input Validation               │ ║
              ║  │     • Security Patterns              │ ║
              ║  └──────────────────────────────────────┘ ║
              ║                                            ║
              ╚════════════════════════════════════════════╝
                                   │
                                   ▼
                         ┌─────────────────┐
                         │                 │
                         │   E2B Sandbox   │
                         │      MCP        │
                         │                 │
                         │  • Execute Code │
                         │  • Test Exploits│
                         │  • Validate Fix │
                         │                 │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   ✅ Validation Pass     │
                    └────────────┬────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────────┐
              │                                      │
              │      GitHub MCP Actions              │
              │                                      │
              │  1. Create security-fix branch       │
              │  2. Commit secure code               │
              │  3. Open Fix Pull Request            │
              │  4. Post security review comment     │
              │                                      │
              └──────────────────┬───────────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────────┐
              │                                      │
              │         📊 FINAL OUTPUT              │
              │                                      │
              │  • PR #N (vulnerable) ← Security     │
              │    review comment                    │
              │                                      │
              │  • PR #N+1 (secure) ← Auto-created   │
              │    fix ready to merge                │
              │                                      │
              └──────────────────────────────────────┘
```

---

## 🔄 Workflow Execution Timeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  0s    Start: Agent discovers new PR #7                            │
│        ├─ Scan vulnerable_app.py                                   │
│        └─ Detect: SQL Injection on line 41                         │
│                                                                     │
│  2s    🔍 Multi-MCP Research Phase                                 │
│        ├─ Perplexity MCP: "SQL Injection CVSS 2024"               │
│        │  └─ Returns: CVSS 9.8 (Critical)                          │
│        │                                                            │
│        └─ Exa MCP: "SQL Injection parameterized queries fix"       │
│           └─ Returns: Real GitHub code examples                    │
│                                                                     │
│  7s    🧠 NVIDIA Nemotron Analysis                                 │
│        └─ Prompt includes:                                         │
│           • Vulnerability details                                  │
│           • Perplexity CVE research                               │
│           • Exa code examples                                      │
│        └─ Output: Risk assessment + recommended actions            │
│                                                                     │
│  12s   🔧 NVIDIA Nemotron Fix Generation                           │
│        └─ Prompt includes:                                         │
│           • Vulnerable code                                        │
│           • Real-world fix patterns from Exa                       │
│        └─ Output: Secure parameterized code                        │
│                                                                     │
│  17s   ✅ E2B Sandbox Validation                                   │
│        ├─ Test SQL injection attack                               │
│        └─ Confirm: Exploit blocked ✅                              │
│                                                                     │
│  21s   🔒 GitHub MCP Automated Remediation                         │
│        ├─ Create branch: security-fix-pr-7                        │
│        ├─ Commit secure code                                       │
│        ├─ Open PR #8                                               │
│        └─ Post review on PR #7                                     │
│                                                                     │
│  24s   ✅ Complete!                                                │
│        └─ Maintainer can now merge PR #8                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

```
PR Files ──────┐
               │
               ├──► Pattern Scanner ──► Vulnerabilities Found
               │
               └──────────────────────────────────┐
                                                  │
CVE Database ◄── Perplexity MCP ◄────────────────┤
                      │                          │
                      ├─ CVSS Scores             │
                      └─ Recent Exploits         │
                                                  │
                                                  │
GitHub Repos ◄── Exa MCP ◄───────────────────────┤
                      │                          │
                      ├─ Safe Code Examples      │
                      └─ Fix Patterns            │
                                                  │
                                                  ▼
                              ┌─────────────────────────────────┐
                              │                                 │
                              │   NVIDIA Nemotron Nano 9B       │
                              │                                 │
                              │   Input Context:                │
                              │   • Vulnerable code             │
                              │   • CVE research                │
                              │   • Real code examples          │
                              │                                 │
                              │   Processing:                   │
                              │   • Risk analysis               │
                              │   • Pattern recognition         │
                              │   • Secure code synthesis       │
                              │                                 │
                              │   Output:                       │
                              │   • Security assessment         │
                              │   • Fixed secure code           │
                              │                                 │
                              └────────────┬────────────────────┘
                                           │
                                           ▼
                              ┌─────────────────────┐
                              │   E2B Sandbox       │
                              │   Validation        │
                              └────────────┬────────┘
                                           │
                                           ▼
                              ┌─────────────────────┐
                              │   GitHub MCP        │
                              │   • Create PR       │
                              │   • Post Review     │
                              └─────────────────────┘
```

---

## 🎯 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Brain** | NVIDIA Nemotron Nano 9B | Vulnerability analysis & code generation |
| **Code Hosting** | GitHub MCP | PR management & automation |
| **Security Research** | Perplexity MCP | CVE & threat intelligence |
| **Code Search** | Exa MCP | Real-world fix examples |
| **Sandbox** | E2B MCP | Safe code execution & testing |
| **Orchestration** | Python + MCP Protocol | Multi-agent coordination |

---

## 🚀 Key Metrics

- **⏱️ Speed**: 8 hours → 24 seconds (1200x faster)
- **🎯 Accuracy**: Pattern + AI + Real examples = High precision
- **🔄 Automation**: 100% autonomous workflow
- **🧠 Context**: 4 MCP sources feeding NVIDIA Nemotron
- **✅ Validation**: Every fix tested in isolated sandbox

---

## 💡 Innovation Highlights

1. **Multi-MCP Orchestration**: First agent to combine 4 different MCPs
2. **Context-Aware AI**: NVIDIA Nemotron with real CVE + code examples
3. **Autonomous Remediation**: Detects → Analyzes → Fixes → Creates PR
4. **Production Ready**: Smart filtering, validation, error handling
