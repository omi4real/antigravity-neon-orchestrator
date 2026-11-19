---
name: consult-neon
description: >-
  Consult Gemini 4 Neon (running locally via gemini-web-to-api) as the Lead
  Software Architect, High-Reasoning Planner, or Principal Debugger. Use when
  tackling complex system architectures, intricate algorithms, subtle bug
  diagnoses, or when planning a multi-step coding task in an Orchestrator flow.
---

# Consult Gemini 4 Neon (Orchestrator Lead Architect)

When working as the executor agent in Antigravity and facing complex architectural
trade-offs, deep mathematical or logical problems, or difficult runtime bugs,
you can consult **Gemini 4 Neon** directly on localhost.

## The CLI Tool: `consult-neon`

The tool is accessible via `consult-neon` in your `$PATH` (or installed to your user bin directory).
It automatically targets `http://127.0.0.1:4981/openai/v1/chat/completions` (or `$GEMINI_WEB_API_URL`),
uses `model: "gemini-4-neon"`, sets `reasoning_effort: "high"`, and sets `X-Antigravity: true`.

### Common Invocations

1. **Architecture & Planning:**
   ```bash
   consult-neon --role planner "Deconstruct the requirements and provide an atomic implementation plan for <task>"
   ```

2. **Debugging an Error or Test Failure:**
   ```bash
   consult-neon --role debugger --context path/to/failing_test.py "The test failed with ValueError: ... What is the root cause and how do we fix it?"
   ```

3. **Code Review:**
   ```bash
   git diff | consult-neon --role reviewer "Review these changes for edge-case bugs and race conditions"
   ```

4. **Structured JSON Output:**
   ```bash
   consult-neon --json --role planner "Output a JSON object with 'tasks': ['step 1', 'step 2'] for building <feature>"
   ```

## The Orchestrator Flow Pattern

1. **Plan:** Call `consult-neon --role planner "<task>"` to receive the architectural blueprint.
2. **Execute:** The executor agent (Antigravity) writes the code, modifies files, and runs commands.
3. **Verify:** Run the automated tests or build checks.
4. **Iterate:** If friction or bugs occur, pass the traceback to `consult-neon --role debugger` to get the exact diagnosis before re-editing.
