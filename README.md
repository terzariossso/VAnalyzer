# ⚡ VAnalyzer

<p align="center">
  <em>A portable, modular CLI tool for system diagnostics, performance auditing, and automated Telegram reporting.</em>
</p>

---

## 📌 Overview
**VAnalyzer** is a lightweight, zero-dependency (in its compiled form) system utility designed for IT professionals and system administrators. It performs deep system diagnostics, analyzes startup bloatware, calculates junk files, and generates comprehensive reports that can be securely exported directly to a private Telegram chat.

## ✨ Key Features
* **Modular Architecture:** The core engine (`dashboard.py` and `registry.py`) is completely decoupled from the test modules. Tests run as isolated child processes via `subprocess`, ensuring that a crash in a hardware test won't take down the main dashboard.
* **Telegram API Integration:** Instantly push diagnostic reports to your phone. 
* **Security First:** API keys (Bot Token and Chat ID) are **never** hardcoded. They are securely stored in a local `.ini` configuration file within the user's `%TEMP%` directory to prevent credential leaks through reverse engineering.
* **Junk & Startup Analysis:** Scans Windows `%TEMP%`, Prefetch, SoftwareDistribution cache, and Recycle Bin, handling OS-level permission exceptions gracefully.
* **Fully Portable:** Compiled into a single standalone `.exe` using PyInstaller. Leaves no footprint on the target machine and runs entirely from memory and temporary directories.

---

## 🚀 How to Use (Portable Version)

The easiest way to use VAnalyzer is to download the pre-compiled binary.
1. Go to the [Releases](../../releases) tab.
2. Download `VAnalyzer.exe`.
3. Run the executable on any Windows machine (no Python installation required).

## 🛠️ Running from Source

If you want to run or modify the Python scripts directly:

    # Clone the repository
    git clone https://github.com/terzariossso/VAnalyzer.git

    # Navigate to the project directory
    cd VAnalyzer

    # Install required dependencies
    pip install -r requirements.txt 

    # Run the dashboard
    python dashboard.py

## 📱 Telegram Bot Setup
To use the `/sendreport` feature, you need to configure your own Telegram bot:
1. Message **@BotFather** on Telegram and create a `/newbot` to get your `BOT_TOKEN`.
2. Message **@GetIDsBot** to get your personal `CHAT_ID`.
3. Start a conversation with your new bot by pressing `Start`.
4. Inside VAnalyzer, run a scan, type `/savereport`, and then `/sendreport`. Enter your credentials when prompted. The tool will save them locally for future use.

## 🧠 Architecture
* `dashboard.py`: The main orchestrator and UI renderer.
* `registry.py`: Centralized command execution and report buffering logic.
* `tests/`: Directory containing dynamic, independent analysis modules.

---
*Developed for system auditing and troubleshooting.*
