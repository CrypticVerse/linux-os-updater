#!/bin/sh

distro=$(grep ^ID= /etc/os-release | cut -d= -f2 | tr -d '"')
if [ "$distro" = "manjaro" ]; then
  distro="archlinux"
fi

# Check if installed using snap
if snap list | grep -q "linux-os-updater"; then
  echo "Updater installed using snap. Running sudo snap refresh..."
  sudo snap refresh "linux-os-updater"
else
  echo "copying update files..."
  sudo wget -O "/usr/bin/$distro-updater.py" "https://github.com/CrypticVerse/linux-os-updater/os/$distro-updater.py"
  sudo wget -O "/usr/bin/update-os-updater.sh" "https://github.com/CrypticVerse/linux-os-updater/tools/update-os-updater.sh"
fi

echo "Script successfully updated! Restart the terminal for changes to take effect."