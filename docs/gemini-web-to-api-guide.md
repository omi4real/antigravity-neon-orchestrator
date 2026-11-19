# gemini-web-to-api Setup & Customization Guide

This guide details how to set up `gemini-web-to-api` as the local backend bridge for **Gemini 4 Neon** and apply the custom orchestration patch.

---

## 1. Why `gemini-web-to-api`?

Users with a consumer Google AI subscription (e.g. Google One AI Premium, or Reliance Jio AI Pro in India) have access to Google's frontier models—**Gemini 4 Neon**, **Gemini 4 Hydrogen**, and **Gemini 4 Carbon**—on [gemini.google.com](https://gemini.google.com). However, agentic developer environments like Google Antigravity or standard IDE plugins often cannot access consumer-entitled Gemini 4 tiers via corporate API keys, marking them as `[Unavailable]`.

`gemini-web-to-api` bridges your authorized Gemini Web session into a local, OpenAI-compatible REST server listening on `http://127.0.0.1:4981`.

---

## 2. What `patches/gemini-web-to-api.patch` Adds

Upstream `gemini-web-to-api` has three critical limitations when interfacing with high-reasoning coding agents:

1. **Model Name Resolution:**
   The Web interface uses internal IDs (`gemini-deeper-analysis` for Neon, `gemini-everyday-help` for Hydrogen, `gemini-code-complex-work` for Carbon). Our patch adds transparent aliases so client requests specifying `gemini-4-neon`, `neon`, or `gemini-neon` route directly without 400 Bad Request errors.

2. **Enforced High-Thinking for Neon:**
   Gemini 4 Neon requires `thinkingLevel = 2` (High) or `4` (Medium). Sending requests with low reasoning or omitting the field causes Google's server to reject the prompt with:
   > *"I seem to be encountering an error. Can I try something else for you?"*
   Our patch automatically injects `thinkingLevel = 2` for Neon and Carbon unless explicitly overridden.

3. **Smart Temporary Mode (Anti-Clutter Engine):**
   In vanilla implementations, every query spawns an empty thread title in the Gemini Web sidebar. Our patch enables request-aware temporary mode:
   - Background audits and EGM reviews run ephemerally (`GEMINI_TEMPORARY=true` / Incognito), keeping your web sidebar 100% clean.
   - Long-form architectural discussions from Antigravity pass `X-Antigravity: true`, retaining persistent session context when needed.

---

## 3. Step-by-Step Installation

### Step 1: Clone the Upstream Repository
```bash
git clone https://github.com/acheong08/gemini-web-to-api.git ~/gemini-web-to-api
cd ~/gemini-web-to-api
```

### Step 2: Apply the Patch
From within the `gemini-web-to-api` repository directory:
```bash
git apply /path/to/antigravity-neon-orchestrator/patches/gemini-web-to-api.patch
```

To verify the patch applied cleanly:
```bash
git status
# You should see modifications in:
#   internal/modules/openai/openai_controller.go
#   internal/modules/openai/openai_service.go
#   internal/modules/providers/gemini_models.go
#   internal/modules/providers/gemini_service.go
```

### Step 3: Extract Session Cookies
1. Open your desktop browser (Chrome, Brave, Edge, Firefox) and navigate to [gemini.google.com](https://gemini.google.com).
2. Ensure you are logged into your Google account with the active AI plan.
3. Open **Developer Tools** (`F12` or `Ctrl+Shift+I` / `Cmd+Option+I`).
4. Go to **Application** (Chrome/Brave/Edge) or **Storage** (Firefox) -> **Cookies** -> `https://gemini.google.com`.
5. Locate and copy the values for:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS` (if present)

*(On Android, you can use Kiwi Browser with the Cookie-Editor extension or extract via DevTools remote debugging).*

### Step 4: Configure `.env`
In `~/gemini-web-to-api`, create or edit `.env`:
```env
PORT=4981
BIND_IP=127.0.0.1
GEMINI_TEMPORARY=true

# Paste your cookies:
COOKIE_1PSID=your_secure_1psid_cookie_here
COOKIE_1PSIDTS=your_secure_1psidts_cookie_here
```

### Step 5: Compile and Run
Ensure Go 1.22+ is installed:
```bash
go build -o gemini-web-to-api .
./gemini-web-to-api
```

You should see:
```
[GIN-debug] Listening and serving HTTP on 127.0.0.1:4981
```

### Step 6: Verify Health & Models
In a new terminal window:
```bash
curl -s http://127.0.0.1:4981/openai/v1/models
```
You should see `gemini-deeper-analysis` listed in the returned JSON.

---

## 4. Running as a Daemon / Background Service

### Linux / systemd
Create `~/.config/systemd/user/gemini-web-to-api.service`:
```ini
[Unit]
Description=Gemini Web to API Bridge
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/gemini-web-to-api
ExecStart=%h/gemini-web-to-api/gemini-web-to-api
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```
Enable and start:
```bash
systemctl --user daemon-reload
systemctl --user enable --now gemini-web-to-api
```

### Android Termux
You can run it in a tmux session or background it:
```bash
nohup ~/gemini-web-to-api/gemini-web-to-api > ~/gemini-web-to-api/gemini.log 2>&1 &
```
Or use Termux:Boot with `~/.termux/boot/start-gemini-bridge.sh`.

### Windows
You can run it in Windows Terminal, background it via PowerShell `Start-Process`, or use [NSSM](https://nssm.cc/) to install it as a Windows Service.
