#!/bin/sh

if [ "$EUID" -ne 0 ]
  then echo "Please run this script as sudo!"
  exit
fi

distro=$(grep ^ID= /etc/os-release | cut -d= -f2 | tr -d '"')
if distro == "manjaro"; then
  distro="archlinux"
  echo "Manjaro is arch based! Run archlinux-updater instead."
  sleep 2
fi

echo "copying update files..."
sudo wget -O "/usr/bin/$distro-updater" "https://github.com/CrypticVerse/linux-os-updater/os/$distro-updater.py"

echo "Script successfully updated! Restart the terminal for changes to take effect."

sudo wget -O "/usr/bin/update-os-updater.sh" "https://github.com/CrypticVerse/linux-os-updater/tools/update-os-updater.sh"