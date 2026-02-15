# Security Triage Agent

Autonomous security vulnerability detection, analysis, and remediation agent powered by NVIDIA Nemotron and multi-MCP orchestration.

## Architecture

```
GitHub PR ──► Pattern Scanner ──► NVIDIA Nemotron (analysis + fix generation)
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
             Perplexity MCP       Exa MCP            E2B Sandbox
             (CVE research)    (code examples)    (exploit validation)
                    │                   │                   │
                    └───────────────────┼───────────────────┘
                                        ▼
                                GitHub MCP ──► Fix PR + Security Review
```

The agent runs a 7-phase pipeline:

1. **Scan** — Reads open PRs via GitHub MCP, detects vulnerability patterns (SQL injection, XSS, etc.) using regex-based static analysis
2. **Research** — Queries Perplexity MCP for recent CVE data and CVSS scores
3. **Code Search** — Queries Exa MCP for real-world fix patterns from open-source repos
4. **Analyze** — Sends vulnerability context + research to NVIDIA Nemotron for root-cause analysis and severity assessment
5. **Fix** — NVIDIA Nemotron generates secure code (e.g., parameterized queries) informed by Exa code examples
6. **Validate** — Reproduces the exploit and tests the fix in an E2B sandbox
7. **Remediate** — Creates a fix branch, commits secure code, opens a PR, and posts a security review comment via GitHub MCP

## Tech Stack

| Component | Technology | Role |
|-----------|-----------|------|
| Core LLM | NVIDIA Nemotron Nano 9B / 70B | Vulnerability analysis, code generation, severity scoring |
| Inference | NVIDIA NIMs API | Model serving via `integrate.api.nvidia.com` |
| PR Management | GitHub MCP | List PRs, read files, create branches, commit code, open PRs, post comments |
| CVE Research | Perplexity MCP | Real-time CVE lookup and threat intelligence |
| Code Search | Exa MCP | Semantic search for fix patterns across GitHub |
| Sandbox | E2B MCP | Isolated code execution for exploit reproduction and fix validation |
| SAST/SCA | Cycode MCP | Static analysis, secrets detection, IaC scanning |
| Browser Testing | DebuggAI MCP | End-to-end exploit testing |
| Dashboard | Streamlit | Real-time scan visualization |
| Orchestration | Python asyncio + MCP Protocol | Async multi-server coordination |

## Key Files

| File | Description |
|------|-------------|
| `auto_pr_scanner.py` | Main agent — auto-scans all open PRs, orchestrates 4 MCP servers |
| `security_triage_agent.py` | 7-phase triage pipeline (scan → research → analyze → fix → validate) |
| `demo_agent.py` | Issue-driven demo agent for single-issue workflow |
| `dashboard_live.py` | Streamlit dashboard with live scan output |
| `vulnerable_app.py` | Intentionally vulnerable Flask app (SQL injection) for testing |
| `vulnerable_app_FIXED.py` | Agent-generated secure version |
| `mcp_orchestrator.py` | MCP server connection manager |
| `requirements.txt` | Python dependencies |

## Setup

### Prerequisites

- Python 3.10+
- Node.js 16+
- Docker (for GitHub MCP server)

### Install

```bash
git clone https://github.com/rajashekarcs2023/secure-opensource.git
cd secure-opensource
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```
NVIDIA_API_KEY=<your-nvidia-api-key>
GITHUB_TOKEN=<your-github-pat>
E2B_API_KEY=<your-e2b-key>
PERPLEXITY_API_KEY=<your-perplexity-key>
EXA_API_KEY=<your-exa-key>
```

## Usage

### Scan all open PRs

```bash
python auto_pr_scanner.py <repo_owner> <repo_name>
```

### Run on a specific GitHub issue

```bash
python demo_agent.py <issue_number>
```

### Run the triage agent on a local file

```bash
python security_triage_agent.py vulnerable_app.py
```

### Launch the dashboard

```bash
streamlit run dashboard_live.py
```

## How It Works

**Auto PR Scanner** (`auto_pr_scanner.py`):

1. Connects to 4 MCP servers (GitHub, E2B, Perplexity, Exa) via async stdio transport
2. Lists all open PRs using GitHub MCP's `list_pull_requests` tool
3. Skips bot-created fix PRs and previously reviewed PRs
4. For each PR with Python files, runs regex-based vulnerability detection
5. Concurrently queries Perplexity (CVE data) and Exa (fix examples)
6. Feeds all context to NVIDIA Nemotron for assessment and fix generation
7. Validates the fix in E2B sandbox by running exploit tests
8. Creates a `security-fix-pr-{N}` branch, commits the fix, opens a new PR, and posts a detailed review comment on the vulnerable PR

**NVIDIA Nemotron is used for**:
- Vulnerability severity assessment with CVSS scoring
- Root-cause analysis of detected patterns
- Context-aware secure code generation (using CVE research + real code examples)
- Security advisory content generation

## License

MIT
