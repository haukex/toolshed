#!/bin/bash
set -euo pipefail

# This script needs to be run as a Startup Application.

# A few other tips on theming Gnome shell:
# $ sudo apt install gnome-shell-extensions gnome-shell-extension-manager
# (Even though this results in two very similar apps being installed, installing the former is necessary to get
# the system's "User Themes" extension installed, and the latter allows installing extensions from the website.)
# Install the "Open Bar" (openbar@neuromorph) extension and configure as desired, in particular the "Auto Themes
# for Dark/Light Modes"; this is the only way I've found so far to dynamically style the top bar. Also, "DM Theme
# Changer" (dm-theme-changer@lynixx01.github.com) allows changing the mouse cursor color schemes.

cur_scheme="$( gsettings get org.gnome.desktop.interface color-scheme )"
dbus-monitor --session "type='signal',interface='org.freedesktop.portal.Settings',member='SettingChanged'" | 
while read -r line; do
    if [[ "$line" =~ "color-scheme" ]]; then
        new_scheme="$( gsettings get org.gnome.desktop.interface color-scheme )"
        if [ "$new_scheme" != "$cur_scheme" ]; then
            uuid="$( gsettings get org.gnome.Terminal.ProfilesList default | perl -wM5.014 -pe 's/^\x27|\x27$//g' )"
            #gsettings list-recursively org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:"$uuid"/
            if [ "$new_scheme" == "'prefer-dark'" ]; then
                gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:"$uuid"/ background-color 'rgb(0,0,0)'
                gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:"$uuid"/ foreground-color 'rgb(255,255,255)'
                gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:"$uuid"/ use-transparent-background true
                gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:"$uuid"/ background-transparency-percent 50
            else
                gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:"$uuid"/ background-color 'rgb(255,255,255)'
                gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:"$uuid"/ foreground-color 'rgb(0,0,0)'
                # Note the following: I tested it, and with my dark background image, low transparencies make colored text hard to read.
                gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:"$uuid"/ use-transparent-background false
            fi
            cur_scheme="$new_scheme"
        fi
    fi
done

