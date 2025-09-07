#!/usr/bin/env zsh

# If external monitor is connected (HDMI-A-1) toggle the internal display
# (eDP-1) according to the laptop lid state.
if [[ "$(hyprctl monitors)" =~ "\sHDMI-A-[0-9]+" ]]; then
  if grep -q "closed" /proc/acpi/button/lid/LID0/state 2>/dev/null; then
    hyprctl keyword monitor "eDP-1,disable"
  else
    hyprctl keyword monitor "eDP-1,preferred,preferred,auto"
  fi
# Otherwise, always make sure the internal display is enabled
else
  hyprctl keyword monitor "eDP-1,preferred,preferred,auto"
fi

