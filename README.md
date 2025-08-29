# dynamic-memory-cleaner
This is a simple Python script for Windows that helps free up RAM by cleaning memory used by background processes. It watches your system’s memory in real time and adjusts how aggressively it frees memory based on usage, aiming to keep things running smoother without causing extra load. Just a neat little helper.

# Dynamic Memory Cleaner for Windows

A lightweight Python script that dynamically optimizes RAM usage on Windows systems.

## 📌 Description

This script frees unused memory (working sets) from all running processes, adjusting its optimization intensity based on real-time memory usage stats. It runs in a continuous loop, checking memory changes every 100ms, and resets intensity to avoid overload.

## ⚙️ Features

- Targets unused working sets across processes
- Adjusts intensity dynamically based on memory pressure
- Runs every 100 milliseconds for near real-time optimization
- Lightweight and requires no external dependencies beyond `psutil`

## 🚀 Requirements

- Windows OS  
- Python 3.7+
- `psutil` module  
  Install via:  
  ```bash
  pip install psutil
🧠 Usage
Clone or download this repository.

Run the script with administrator privileges:

bash
Copiar código
python memory_cleaner.py
Alternatively, create a .bat file to run it automatically:

bat
Copiar código
@echo off
cd "C:\path\to\script"
python memory_cleaner.py
💡 Right-click the .bat file and run as administrator.

⚠️ Note
This tool is experimental. While it may reduce memory pressure, use with caution and monitor system performance.

