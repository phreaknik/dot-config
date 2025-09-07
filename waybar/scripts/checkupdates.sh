#!/usr/bin/bash

# Get number of paru updates
num_paru_updates=$(paru -Qu | wc -l)

# Get number of flatpak updates
num_flatpak_updates=$(flatpak remote-ls --updates 2>/dev/null | grep -v "Application ID" | wc -l)

# Calculate total updates
num_updates=$((num_paru_updates + num_flatpak_updates))

# Output for waybar
if [ "$num_updates" -eq 0 ]; then
    echo '{"text": "Up to date!", "alt": "up-to-date", "class": "up-to-date", "tooltip": "System is up to date"}'
else
    if [ "$num_updates" -eq 1 ]; then
        text="1 update"
    else
        text="$num_updates updates"
    fi
    
    tooltip="Paru: $num_paru_updates updates\\nFlatpak: $num_flatpak_updates updates"
    echo "{\"text\": \"$text\", \"alt\": \"updates-pending\", \"class\": \"updates-pending\", \"tooltip\": \"$tooltip\"}"
fi
