# Antigravity Neon Orchestrator & EGM Review Loop

A cross-platform orchestration layer bridging **Google Antigravity** with **Gemini 4 Neon** running via a local Web-to-API proxy.

Provides dual capabilities:
1. **Top-Down Orchestrator Planning (`consult-neon`)**: Consults Gemini 4 Neon with high thinking as the Lead Architect, High-Reasoning Planner, or Principal Debugger.
2. **Bottom-Up Stateless Auditing (`egm-goldfish`)**: Implements the Elephant-Goldfish Model (EGM), using Gemini 4 Neon to cold-audit design specifications, implementation plans, and code diffs with zero accumulated historical bias.

---

## Architecture Overview

```
                      +---------------------------------------+
                      |         Google Antigravity            |
                      |  (Executor / Elephant Context Keeper)  |
                      +---------------------------------------+
                                     |         ^
          Top-Down Architecture Plan |         | Cold Audit Findings
         (Atomic Checklist, Schema)  |         | (Blocker / Major / Nit)
                                     v         |
                      +---------------------------------------+
                      |  CLI Bridge (consult-neon / goldfish) |
                      +---------------------------------------+
                                          |
                        HTTP / OpenAI-compatible endpoint
                                          v
                      +---------------------------------------+
                      |       gemini-web-to-api (Port 4981)   |
                      |  - Model Alias Mapping                |
                      |  - Enforced High Thinking for Neon    |
                      |  - Ephemeral / Incognito Clutter-Free |
                      +---------------------------------------+
                                          |
                                          v
                      +---------------------------------------+
                      |         Gemini 4 Neon Engine          |
                      |     (High-Reasoning Frontier LLM)     |
                      +---------------------------------------+
```

---

## Key Features

- **Dynamic Model Aliasing**: Routes requests for `gemini-4-neon`, `neon`, and `gemini-neon` to the underlying web backend identifier (`gemini-deeper-analysis`).
- **Enforced Reasoning**: Guarantees high thinking effort (`thinkingLevel = 2`) for Neon requests to prevent backend validation errors.
- **Smart Temporary Mode**: Automatically runs background audits and review passes in ephemeral mode (`GEMINI_TEMPORARY=true`) so web chat history remains clean.
- **Stateless Personas**: Includes prompt personas for Design Critic, Implementation Readiness, Codebase Details, Structural Validation, and System Boundary verification.
- **Cross-Platform**: Runs on Android Termux, Linux, macOS, and Windows.
- **Configurable Endpoints**: Defaults to `http://127.0.0.1:4981/openai/v1/chat/completions`, overridable via the `GEMINI_WEB_API_URL` environment variable.

---

## Quickstart

### 1. Prerequisites
- Python 3.7+ (Standard library only; no pip dependencies required)
- Go 1.22+ (to compile `gemini-web-to-api`)
- Active Google account with Gemini 4 access (e.g., Google One AI Premium or partner plan)

### 2. Backend Proxy Setup
Follow [docs/gemini-web-to-api-guide.md](docs/gemini-web-to-api-guide.md) to set up the local bridge:
1. Clone `gemini-web-to-api`.
2. Apply `patches/gemini-web-to-api.patch`.
3. Provide your session cookies (`__Secure-1PSID`) in `.env`.
4. Compile and launch the binary on port 4981.

### 3. Install Tools & Skills
Clone this repository and run the cross-platform installer:

```bash
git clone https://github.com/omi4real/antigravity-neon-orchestrator.git
cd antigravity-neon-orchestrator
python3 install.py
```

The installer will:
- Copy `bin/consult-neon` and `bin/egm-goldfish` to your user bin directory (`$PREFIX/bin` on Termux, `~/.local/bin` on Linux/macOS, `%LOCALAPPDATA%` with `.cmd` shims on Windows).
- Register skills with your local Antigravity installation.
- Verify connectivity to the local proxy service on port 4981.

---

## CLI Reference

### Consult Neon (Architect & Planner)
```bash
# Architecture & Planning
consult-neon --role planner "Design an event-driven task queue with retries"

# Principal Debugger
consult-neon --role debugger --context error.log "Explain why this deadlock occurs"

# Code Review
git diff | consult-neon --role reviewer "Review this changeset for edge cases"

# Structured JSON Output
consult-neon --json --role planner "Output atomic implementation steps in JSON"
```

### EGM Goldfish Review (Stateless Auditor)
```bash
# List all available reviewer personas
egm-goldfish --list-personas

# Audit a design specification against feature standards
egm-goldfish docs/spec.md --persona design_critic

# Check implementation readiness before writing code
egm-goldfish plan.md --persona implementation_readiness

# Audit a git diff cold with zero context assumptions
git diff | egm-goldfish --persona design_critic -
```

---

## Autonomous Agent Setup

To set up this stack on a new device using an Antigravity agent, copy and paste the prompt in [bootstrap-prompt.md](bootstrap-prompt.md) into your agent chat.

---

## Repository Structure

```
antigravity-neon-orchestrator/
├── bin/
│   ├── consult-neon             # Top-down orchestrator planner CLI
│   └── egm-goldfish             # Stateless Goldfish review CLI
├── skills/
│   ├── consult-neon/SKILL.md    # Antigravity skill for planning
│   └── egm-goldfish/SKILL.md    # Antigravity skill for auditing
├── patches/
│   └── gemini-web-to-api.patch  # Model aliases & thinking patches
├── docs/
│   ├── spec.md                  # Comprehensive architectural spec
│   ├── gemini-web-to-api-guide.md # Proxy setup & cookie instructions
│   └── cross-platform-guide.md  # OS-specific installation notes
├── install.py                   # Cross-platform installer
├── install.sh                   # Unix shell wrapper
└── bootstrap-prompt.md          # Autonomous agent bootstrap prompt
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
