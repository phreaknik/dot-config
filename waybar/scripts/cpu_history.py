#!/usr/bin/env python3
"""CPU Usage Graph Monitor - Displays a unicode graph of CPU usage history."""

import json
import psutil
from pathlib import Path

# Configuration
HISTORY_FILE = Path.home() / ".cpu_usage_history.json"
HISTORY_DEPTH = 20
BAR_CHARS = ' ▁▂▃▄▅▆▇█'

def main():
    # Load history
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE) as f:
                data = json.load(f)
                # Handle both old format (dict with 'history' key) and new format (list)
                if isinstance(data, dict):
                    history = [item['usage'] if isinstance(item, dict) else item 
                              for item in data.get('history', [])]
                elif isinstance(data, list):
                    history = data
        except (json.JSONDecodeError, IOError, ValueError):
            pass
    
    # Update with current CPU usage
    history.append(psutil.cpu_percent(interval=0.1))
    history = history[-HISTORY_DEPTH:]
    
    # Save history
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)
    
    # Generate graph
    # Pad history if needed
    padded = [0] * (HISTORY_DEPTH - len(history)) + history
    
    # Convert to bar characters
    bars = ''.join(BAR_CHARS[int(v / 100 * (len(BAR_CHARS) - 1))] for v in padded)
    
    # Output (uncomment the line you prefer)
    print(f"[{bars}]")  # Compact version
    # print(f"[{bars}] {history[-1]:3.0f}%")  # With percentage

if __name__ == "__main__":
    main()
