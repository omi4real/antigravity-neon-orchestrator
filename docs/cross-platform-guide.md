# Cross-Platform Deployment Guide

This guide covers deployment and integration details across **Android Termux**, **Linux**, **macOS**, and **Windows**.

---

## 1. Android Termux

Termux is a complete Linux environment running on Android without requiring root access.

### Prerequisites
```bash
pkg update && pkg install git python golang
```

### Shebang Resolution
On Android Termux, standard Linux paths like `/bin/bash` and `/usr/bin/env` do not exist. Binaries must use Termux-native paths (e.g. `/data/data/com.termux/files/usr/bin/python3`).
The installer (`install.py`) automatically detects Termux and rewrites shebangs accordingly. If you move scripts manually, run:
```bash
termux-fix-shebang bin/*
```

### Background Daemon
To keep `gemini-web-to-api` running reliably without being killed by Android battery optimizations:
1. In Android App Info for Termux, set **Battery Usage** to **Unrestricted**.
2. Run in a persistent tmux session or via `nohup`:
   ```bash
   nohup ~/gemini-web-to-api/gemini-web-to-api > ~/gemini-web-to-api/gemini.log 2>&1 &
   ```
3. (Optional) Install `Termux:Boot` from F-Droid to launch the daemon on phone reboot.

---

## 2. Linux (Debian, Ubuntu, Arch, Fedora)

### Prerequisites
```bash
# Debian / Ubuntu
sudo apt update && sudo apt install -y git python3 golang curl

# Arch Linux
sudo pacman -S git python go curl

# Fedora
sudo dnf install -y git python3 golang curl
```

### PATH Setup
The installer places binaries into `~/.local/bin`. Ensure this directory is in your `$PATH`:
```bash
# Add to ~/.bashrc or ~/.zshrc if not present:
export PATH="$HOME/.local/bin:$PATH"
```

### Systemd User Service
Run `gemini-web-to-api` as a managed background service:
```bash
mkdir -p ~/.config/systemd/user
cat << 'EOF' > ~/.config/systemd/user/gemini-web-to-api.service
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
EOF

systemctl --user daemon-reload
systemctl --user enable --now gemini-web-to-api
```

---

## 3. macOS (Apple Silicon & Intel)

### Prerequisites
Install dependencies via [Homebrew](https://brew.sh/):
```bash
brew install git python go curl
```

### PATH Setup
Binaries are placed in `~/.local/bin`. On macOS with zsh (default), ensure `~/.zshrc` has:
```zsh
export PATH="$HOME/.local/bin:$PATH"
```

### Launchd Daemon
To run automatically on macOS login, create `~/Library/LaunchAgents/com.antigravity.gemini-bridge.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.antigravity.gemini-bridge</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/gemini-web-to-api/gemini-web-to-api</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/gemini-web-to-api</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```
Load the agent:
```bash
launchctl load ~/Library/LaunchAgents/com.antigravity.gemini-bridge.plist
```

---

## 4. Windows (WSL & Native)

### Option A: Windows Subsystem for Linux (WSL 2) — Recommended
If you use Antigravity or VS Code inside WSL, follow the standard **Linux** instructions inside your WSL terminal (e.g. Ubuntu). `http://127.0.0.1:4981` binds seamlessly across host and WSL.

### Option B: Native Windows (PowerShell / Command Prompt)

1. **Install Prerequisites:**
   - Install **Python 3** from [python.org](https://www.python.org/) (ensure **"Add Python to PATH"** is checked).
   - Install **Go** from [go.dev](https://go.dev/dl/).
   - Install **Git for Windows**.

2. **Run Installer:**
   Open PowerShell and execute:
   ```powershell
   cd antigravity-neon-orchestrator
   python install.py
   ```
   The installer automatically creates Windows Command Prompt shims (`consult-neon.cmd` and `egm-goldfish.cmd`) alongside the Python scripts.

3. **Running the Bridge:**
   ```powershell
   cd ~/gemini-web-to-api
   go build -o gemini-web-to-api.exe .
   .\gemini-web-to-api.exe
   ```
   Or use [NSSM (Non-Sucking Service Manager)](https://nssm.cc/) to install it as a Windows Background Service.
