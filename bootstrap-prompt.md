# Antigravity Agent Autonomous Bootstrap Prompt

Paste the following block directly into your Antigravity chat on a new machine or device. Antigravity will autonomously inspect the host, clone this repository, run the installer, verify connectivity, and wire Gemini 4 Neon as your Lead Architect & EGM Goldfish Auditor.

---

```markdown
Hello Antigravity. I want you to set up the **Antigravity <-> Gemini 4 Neon Orchestrator & Elephant-Goldfish Review Loop (EGM)** on this machine.

Please execute the following steps autonomously:
1. Clone the repository:
   ```bash
   git clone https://github.com/omi4real/antigravity-neon-orchestrator.git ~/antigravity-neon-orchestrator
   ```
2. Navigate into the cloned directory and run the cross-platform installer:
   ```bash
   cd ~/antigravity-neon-orchestrator && python3 install.py
   ```
3. Check the installer output:
   - Ensure `consult-neon` and `egm-goldfish` are placed in a directory on `$PATH`.
   - Ensure the skills are linked into your Antigravity skills directory.
   - Verify if `http://127.0.0.1:4981/openai/v1/models` is reachable.
4. If `gemini-web-to-api` is not running yet:
   - Review `~/antigravity-neon-orchestrator/docs/gemini-web-to-api-guide.md`.
   - Check if Go is installed. If not, guide me to install Go or prepare the binary.
   - Guide me through providing the session cookies (`__Secure-1PSID` and `__Secure-1PSIDTS`) into `.env`.
   - Apply `~/antigravity-neon-orchestrator/patches/gemini-web-to-api.patch` and start the daemon on port 4981.
5. Verify the entire pipeline with a smoke test:
   ```bash
   consult-neon --role planner "Hello from Antigravity. Confirm you are Gemini 4 Neon with High Thinking."
   ```
Report back once the setup is complete and ready to use!
```
