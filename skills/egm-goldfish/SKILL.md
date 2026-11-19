---
name: egm-goldfish
description: >-
  Stateless Goldfish Review Loop using Gemini 4 Neon via local EGM.
  Audits technical specifications, implementation plans, architecture designs,
  and git diffs cold with ZERO historical bias and deep reasoning.
---

# EGM Goldfish Review: Stateless Quality & Assumption Audit

In the Elephant-Goldfish Model (EGM), Antigravity acts as the **Elephant** (holding
your project context and drafting specifications), while **Gemini 4 Neon** acts
as the **Goldfish** (a stateless reviewer with zero historical baggage).

## The CLI Tool: `egm-goldfish`

The CLI tool is accessible as `egm-goldfish` in your `$PATH`.
It loads Google EGM personas from bundled `agents/` or `~/.gemini/config/plugins/egm/agents/`,
attaches standards from `resources/document_standards/`, and queries Gemini 4 Neon
with high reasoning effort.

### Available Reviewer Personas

| Persona | Focus | Standard Applied |
| :--- | :--- | :--- |
| `design_critic` (or `design`) | Architectural risks, scalability, security, cost | `feature-spec-standard.md` |
| `implementation_readiness` (or `readiness`) | Actionability, missing schemas, clarity for coder | `implementation-readiness-standard.md` |
| `structural` | Document organization, completeness, compliance | `feature-spec-standard.md` |
| `comprehension` | Unstated assumptions, ambiguous wording, jargon | Self-contained |
| `codebase_details` (or `codebase`) | Compatibility with real code, imports, APIs | Real codebase files |
| `zoom_out` (or `zoom-out`) | Strategic fit, cross-system boundaries, scope | `zoom-out-standard.md` |

### How to Use

1. **Review a Design Specification:**
   ```bash
   egm-goldfish docs/design_draft.md --persona design_critic
   ```

2. **Verify Implementation Readiness before Coding:**
   ```bash
   egm-goldfish docs/plan.md --persona implementation_readiness
   ```

3. **Audit a Git Diff or Patch Cold:**
   ```bash
   git diff | egm-goldfish --persona design_critic -
   ```

4. **Brainstorming Concept Audit (Pre-Draft):**
   ```bash
   egm-goldfish concept.md --persona design_critic --mode BRAINSTORM
   ```

## The Verification Loop

1. **Draft:** The Elephant (Antigravity) writes or updates the spec/diff.
2. **Audit:** Run `egm-goldfish <file> --persona <name>`.
3. **Reconcile:** The Elephant reviews all `[Blocker]` and `[Major]` findings, resolves each deficiency, and re-audits until verified clean.
