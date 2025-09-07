#!/usr/bin/env zsh

# By default, leave internal display enabled
should_disable=false

# If external monitor is connected (HDMI-A-1) toggle the internal display
# (eDP-1) according to the laptop lid state.
if [[ "$(hyprctl monitors)" =~ "\sHDMI-A-[0-9]+" ]]; then
  if grep -q "closed" /proc/acpi/button/lid/LID0/state 2>/dev/null; then
    should_disable=true
  fi
fi

if $should_disable; then
  echo "DISABLE"
  hyprctl keyword monitor "eDP-1,disable"
  hyprctl dispatch workspace 0
else
  echo "ENABLE"
  hyprctl keyword monitor "eDP-1,preferred,preferred,auto"
fi
