#!/usr/bin/env python3
"""
install.py: Cross-Platform Installer for Antigravity Neon Orchestrator & EGM Bridge.

Supports:
- Android Termux
- Linux (Ubuntu, Debian, Fedora, Arch, Alpine, etc.)
- macOS (Intel & Apple Silicon)
- Windows (WSL and Native Windows via Python/CMD wrappers)

Usage:
    python3 install.py
    python3 install.py --bin-dir ~/.local/bin
"""

import argparse
import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import urllib.error
import urllib.request

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def is_termux():
    return bool(os.environ.get("TERMUX_VERSION") or "/data/data/com.termux" in sys.executable or os.path.exists("/data/data/com.termux"))


def is_windows():
    return platform.system() == "Windows"


def get_default_bin_dir():
    if is_termux():
        prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
        termux_bin = os.path.join(prefix, "bin")
        if os.path.isdir(termux_bin) and os.access(termux_bin, os.W_OK):
            return termux_bin

    home = os.path.expanduser("~")
    local_bin = os.path.join(home, ".local", "bin")
    return local_bin


def make_executable(path):
    try:
        current_stat = os.stat(path)
        os.chmod(path, current_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except Exception as e:
        print(f"  [!] Notice: could not chmod {path}: {e}")


def fix_shebang_if_termux(filepath):
    if not is_termux():
        return
    prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    termux_python = os.path.join(prefix, "bin", "python3")
    if not os.path.exists(termux_python):
        termux_python = sys.executable

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if lines and lines[0].startswith("#!"):
            lines[0] = f"#!{termux_python}\n"
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(lines)
    except Exception as e:
        print(f"  [!] Notice: Could not rewrite shebang for {filepath}: {e}")


def install_binaries(bin_dir):
    print(f"[*] Installing CLI binaries to: {bin_dir}")
    os.makedirs(bin_dir, exist_ok=True)

    bin_source_dir = os.path.join(REPO_ROOT, "bin")
    binaries = ["consult-neon", "egm-goldfish"]

    for b in binaries:
        src = os.path.join(bin_source_dir, b)
        dst = os.path.join(bin_dir, b)
        shutil.copy2(src, dst)
        fix_shebang_if_termux(dst)
        make_executable(dst)
        print(f"  [+] Installed {b} -> {dst}")

        # On Windows, generate .cmd launcher shim
        if is_windows():
            cmd_shim = os.path.join(bin_dir, f"{b}.cmd")
            with open(cmd_shim, "w", encoding="utf-8") as f:
                f.write(f'@echo off\npython "%~dp0\\{b}" %*\n')
            print(f"  [+] Created Windows shim -> {cmd_shim}")

    # Check PATH
    path_dirs = [os.path.abspath(p) for p in os.environ.get("PATH", "").split(os.pathsep)]
    if os.path.abspath(bin_dir) not in path_dirs:
        print("\n  [!] WARNING: Bin directory is not in your current $PATH.")
        if is_windows():
            print(f"      Add '{bin_dir}' to your user Environment Variables (Path).")
        else:
            print(f"      Run: export PATH=\"{bin_dir}:$PATH\"")
            print(f"      And add it to your shell rc file (~/.bashrc or ~/.zshrc).")


def check_egm_plugin():
    egm_dir = os.path.expanduser("~/.gemini/config/plugins/egm")
    if os.path.isdir(egm_dir):
        print(f"  [✓] Google EGM plugin detected at: {egm_dir}")
    else:
        print("  [i] Google EGM plugin not detected.")
        print("      To install reviewer personas: agy plugin install https://github.com/google/elephant-go")


def install_skills():
    home = os.path.expanduser("~")
    # Search for known Antigravity skill directories
    candidate_plugin_dirs = [
        os.path.join(home, ".gemini", "config", "plugins", "neon-orchestrator", "skills"),
        os.path.join(home, ".gemini", "antigravity-cli", "builtin", "skills"),
    ]

    skills_source = os.path.join(REPO_ROOT, "skills")
    if not os.path.isdir(skills_source):
        return

    skills = [s for s in os.listdir(skills_source) if os.path.isdir(os.path.join(skills_source, s))]

    for target_dir in candidate_plugin_dirs:
        try:
            os.makedirs(target_dir, exist_ok=True)
            for skill_name in skills:
                src = os.path.join(skills_source, skill_name)
                dst = os.path.join(target_dir, skill_name)
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"  [+] Installed Antigravity skill '{skill_name}' -> {dst}")
        except Exception as e:
            print(f"  [!] Notice: could not write to {target_dir}: {e}")


def check_health(api_url="http://127.0.0.1:4981"):
    models_url = f"{api_url.rstrip('/')}/openai/v1/models"
    print(f"\n[*] Checking gemini-web-to-api connection at: {models_url}")
    try:
        req = urllib.request.Request(models_url, headers={"User-Agent": "Antigravity-Installer/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("id", "") for m in data.get("data", [])]
            print(f"  [✓] Bridge is LIVE! ({len(models)} models available)")

            neon_found = any("neon" in m.lower() or "deeper-analysis" in m.lower() for m in models)
            if neon_found:
                print("  [✓] Gemini 4 Neon (gemini-deeper-analysis) backend is active and recognized.")
            else:
                print("  [!] Notice: Gemini 4 Neon backend was not found in the model list.")
            return True
    except urllib.error.URLError:
        print(f"  [!] Bridge is NOT running on {api_url}.")
        print("      To launch the bridge:")
        print("      1. Follow docs/gemini-web-to-api-guide.md to set up cookies.")
        print("      2. Apply patches/gemini-web-to-api.patch to your gemini-web-to-api repo.")
        print("      3. Run ./gemini-web-to-api")
        return False
    except Exception as e:
        print(f"  [!] Bridge check encountered an unexpected error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Install Antigravity Neon Orchestrator & EGM Bridge")
    parser.add_argument("--bin-dir", default=get_default_bin_dir(), help="Directory to install executables")
    parser.add_argument("--api-url", default="http://127.0.0.1:4981", help="URL of gemini-web-to-api daemon")
    parser.add_argument("--no-skills", action="store_true", help="Skip registering Antigravity skills")
    parser.add_argument("--skip-check", action="store_true", help="Skip connectivity check")

    args = parser.parse_args()

    print("=" * 70)
    print(" Antigravity <-> Gemini 4 Neon Orchestrator & EGM Bridge Installer")
    print("=" * 70)
    print(f"Platform: {platform.system()} ({platform.machine()})")
    print(f"Termux Environment: {'Yes' if is_termux() else 'No'}\n")

    install_binaries(args.bin_dir)
    check_egm_plugin()

    if not args.no_skills:
        install_skills()

    if not args.skip_check:
        check_health(args.api_url)

    print("\n" + "=" * 70)
    print(" Setup Complete!")
    print(" Usage:")
    print("   consult-neon --role planner \"Your prompt here\"")
    print("   egm-goldfish <file> --persona design_critic")
    print("=" * 70)


if __name__ == "__main__":
    main()
