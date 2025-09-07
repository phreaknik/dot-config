#!/usr/bin/env zsh

# If external monitor is connected (HDMI-A-1) allow enable/disable of internal
# display (eDP-1)
if [[ "$(hyprctl monitors)" =~ "\sHDMI-A-[0-9]+" ]]; then
  if [[ $1 == "close" ]]; then
    hyprctl keyword monitor "eDP-1,disable"
  else
    hyprctl keyword monitor "eDP-1,preferred,preferred,auto"
  fi
# Otherwise, always make sure the internal display is enabled
else
  hyprctl keyword monitor "eDP-1,preferred,preferred,auto"
fi
