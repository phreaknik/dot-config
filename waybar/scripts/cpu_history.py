#!/usr/bin/env python3
"""CPU Usage Graph Monitor - Displays a unicode graph of CPU usage history."""
import json
import os
import sys
import psutil

# Configuration
CACHE_DIR = os.path.expanduser(os.environ.get('XDG_CACHE_HOME', '~/.cache'))
HISTORY_FILE = os.path.join(CACHE_DIR, 'cpu_usage_history.json')
HISTORY_DEPTH = 20
BAR_CHARS = ' ▁▂▃▄▅▆▇█'
BAR_LEVELS = len(BAR_CHARS) - 1

def main():
    # Ensure cache directory exists
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Load existing data
    try:
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
            # Handle legacy format
            if isinstance(data, list):
                data = {"history": data, "show_graph": True}
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"history": [], "show_graph": True}
    
    # Handle toggle command
    if len(sys.argv) > 1 and sys.argv[1] == "toggle":
        data["show_graph"] = not data.get("show_graph", True)
        with open(HISTORY_FILE, 'w') as f:
            json.dump(data, f)
        return
    
    # Get CPU usage (single measurement for both current and per-core)
    per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    current_usage = sum(per_core) / len(per_core)  # Average of cores
    
    # Update history
    history = data.get("history", [])
    history.append(current_usage)
    if len(history) > HISTORY_DEPTH:
        history = history[-HISTORY_DEPTH:]
    
    # Generate output
    if data.get("show_graph", True):
        # Build graph efficiently
        graph = []
        for i in range(HISTORY_DEPTH):
            if i < HISTORY_DEPTH - len(history):
                graph.append(' ')
            else:
                val = history[i - (HISTORY_DEPTH - len(history))]
                graph.append(BAR_CHARS[min(int(val * BAR_LEVELS / 100), BAR_LEVELS)])
        text = f"[{''.join(graph)}]"
    else:
        text = f"{current_usage:.1f}%"
    
    # Build tooltip
    tooltip = '\n'.join(f"Core {i}: {usage:.1f}%" for i, usage in enumerate(per_core))
    
    # Save updated data
    data["history"] = history
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f)
    
    # Output for waybar
    print(json.dumps({
        "text": text,
        "tooltip": tooltip,
        "class": "cpu-history"
    }))

if __name__ == "__main__":
    main()
