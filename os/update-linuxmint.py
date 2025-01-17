import sys
import subprocess
import re
from version_mapping import LINUXMINT_VERSIONS

def get_current_number():
    try:
        result = subprocess.run(['lsb_release', '-r'], capture_output=True, text=True, check=True)
        match = re.search(r'Release:\s+(\S+)', result.stdout)
        if match:
            return match.group(1)
        else:
            print("Could not determine the current Mint version.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error running lsb_release.")
        sys.exit(1)

def compare(current, updated):
    currentParts = list(map(int, current.split('.')))
    updatedParts = list(map(int, updated.split('.')))

    if currentParts[0] < updatedParts[0]:
        return -1
    elif currentParts[0] > updatedParts[0]:
        return 1
    else:
        if currentParts[1] < updatedParts[1]:
            return -1
        elif currentParts[1] > updatedParts[1]:
            return 1
    return 0        

def run_sys_update():
    try:
        print("Running system upgrade...")
        subprocess.run("sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y", shell=True, check=True)
        subprocess.run("sudo apt autoremove --purge -y && sudo apt install mintupgrade", shell=True, check=True)
        subprocess.run("sudo mintupgrade check && sudo mintupgrade download && sudo mintupgrade upgrade", shell=True, check=True)
        print("System download completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during pacman operations: {e}. Did you run as root?")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: update-linuxmint <version>")
        sys.exit(1)

    version = sys.argv[1] 
    current_version = get_current_number()  

    if version not in LINUXMINT_VERSIONS:
        print(f"Invalid version: {version}")
        sys.exit(1)

    sorted_versions = sorted(LINUXMINT_VERSIONS.keys(), key=lambda x: list(map(int, x.split('.'))))

    if version == sorted_versions[0]:
        print(f"You are on the latest stable release ({version}). No update needed.")
        sys.exit(0)
    elif compare(current_version, version) >= 0:
        print(f"Your current version ({current_version}) is higher than the target version ({version}). No update needed.")
        sys.exit(0)  

    print(f"\033[33mWarning: This program WILL reboot your system. Are you sure you want to continue?\033[0m")
    choice = input("continue? [y/N] ").strip().lower()
    if choice in ['n', 'no']:
        print("exiting...")
        sys.exit(1)      

    run_sys_update()
    print("Rebooting...")
    subprocess.run("sudo reboot", shell=True, check=True)

if __name__ == "__main__":
    main()