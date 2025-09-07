#!/usr/bin/env python3
"""CPU Usage Graph Monitor - Displays a unicode graph of CPU usage history."""
import json
import os
import psutil

# Configuration
CACHE_DIR = os.path.expanduser(os.environ.get('XDG_CACHE_HOME', '~/.cache'))
HISTORY_FILE = f"{CACHE_DIR}/cpu_usage_history.json"
HISTORY_DEPTH = 20
BAR_CHARS = ' ▁▂▃▄▅▆▇█'
BAR_MAX = len(BAR_CHARS) - 1

def main():
    # Ensure cache directory exists
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Load history
    history = []
    try:
        with open(HISTORY_FILE, 'rb') as f:
            data = json.load(f)
            # Handle both old and new formats
            if isinstance(data, list):
                history = data
            else:
                history = [item['usage'] if isinstance(item, dict) else item 
                          for item in data.get('history', [])]
    except:
        pass
    
    # Update with current CPU usage
    history.append(psutil.cpu_percent(interval=0.1))
    history = history[-HISTORY_DEPTH:]
    
    # Save history
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)
    
    # Generate graph
    # Pad and convert to bars in one pass
    pad_count = HISTORY_DEPTH - len(history)
    bars = '0' * pad_count + ''.join(BAR_CHARS[int(v * BAR_MAX / 100)] for v in history)
    bars = bars.replace('0', ' ')
    
    print(f"[{bars}]")

if __name__ == "__main__":
    main()
