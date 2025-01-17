#!/bin/python3
import sys
import subprocess
import re

def warn_reboot():
    print(f"\033[33mWarning: This program WILL reboot your system. Are you sure you want to continue?\033[0m")
    choice = input("continue? [y/N] ").strip().lower()
    if choice in ['n', 'no']:
        print("exiting...")
        sys.exit(1)


def get_pop_version():
    try:
        result = subprocess.run(['lsb_release', '-r'], capture_output=True, text=True, check=True)
        match = re.search(r'Release:\s+(\S+)', result.stdout)
        if match:
            return match.group(1)
        else:
            print("Could not determine the current Pop!_OS version.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error running lsb_release.")
        sys.exit(1)

def runUpdate():
    try:
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'full-upgrade'], check=True)
        subprocess.run(['pop-upgrade', 'recovery', 'upgrade', 'from-release'], check=True)
        subprocess.run("yes | pop-upgrade release upgrade", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Error running apt.")
        sys.exit(1)

def old_popos_functions():
    subprocess.run("sudo sed -i 's/us.archive/old-releases/g' /etc/apt/sources.list", shell=True, check=True)
    subprocess.run("sudo apt update -m && sudo dpkg --configure -a", shell=True, check=True)
    subprocess.run("sudo apt install -f && sudo apt full-upgrade && sudo apt install -y pop-desktop", shell=True, check=True)
    subprocess.run("sudo mkdir -p /etc/apt/backup && sudo mv /etc/apt/sources.list.d/* /etc/apt/backup", shell=True, check=True)
    subprocess.run("sudo add-apt-repository -yn ppa:system76/pop", shell=True, check=True)
    subprocess.run("sudo sed -i 's/old-releases/us.archive/g' /etc/apt/sources.list && sudo sed -Ei 's/cosmic|eoan|disco/focal/g' /etc/apt/sources.list /etc/apt/sources.list.d/*.list", shell=True, check=True)
    subprocess.run("sudo apt update && sudo apt install -y dpkg apt && sudo apt full-upgrade 2>/dev/null | tee ~/upgrade.log", shell=True, check=True)

def update_old_popos():
    print(f"\033[33mThis will update your system to Pop!_OS 20.04\033[0m")
    print(f"\033[33mAfter this, you will need to run this tool again to update to 22.04\033[0m")
    warn_reboot()
    try:
        old_popos_functions()
    except subprocess.CalledProcessError:
        print("Error running programs.")
        sys.exit(1)    

def main():
    if get_pop_version() <= '19.10':
        update_old_popos()
        subprocess.run("sudo reboot", shell=True, check=True)
    elif get_pop_version() == '20.10':
        print("Follow the guide on the Pop!_OS website to update to 22.04")
        sys.exit(1)

    if len(sys.argv) != 1:
        print("Usage: popos-updater")
        print("This script does not take any arguments.")
        print("Pop!_OS does not have specific version upgrades, so this script will update your system to the latest version.")
        sys.exit(1)

    pop_version = get_pop_version()
    if pop_version == '22.04':
        print("You are already on the latest version of Pop!_OS.")
        sys.exit(1)

    warn_reboot()

    runUpdate()
    subprocess.run("sudo reboot", shell=True, check=True)

if __name__ == '__main__':
    main()
