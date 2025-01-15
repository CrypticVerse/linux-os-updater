#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run this script as sudo!"
  exit
fi

echo "Welcome to Linux OS Updater!"
sleep 2

echo "Setting up files..."

curl -fsSL https://github.com/CrypticVerse/linux-os-updater/tools/update-os-updater.sh | bash