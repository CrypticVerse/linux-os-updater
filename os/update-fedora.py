#!/bin/python3
import os
import sys
import re
import subprocess
from extra_functions import *

def get_fedora_version():
    try:
        result = subprocess.run(['lsb_release', '-r'], capture_output=True, text=True, check=True)
        match = re.search(r'Release:\s+(\S+)', result.stdout)
        if match:
            return match.group(1)
        else:
            print("Could not determine the current Fedora version.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error running lsb_release.")
        sys.exit(1)

def run_upgrade(version):
    print("Upgrading the system...")
    subprocess.run("sudo dnf install dnf-plugin-system-upgrade lsb-release -y", shell=True, check=True)
    subprocess.run('sudo dnf upgrade --refresh -y', shell=True, check=True)
    subprocess.run(f"sudo dnf system-upgrade download --releasever={version} --allowerasing -y", shell=True, check=True)
    subprocess.run("sudo dnf system-upgrade reboot", shell=True, check=True)

def main():
    echo_distro("fedora", version=True)
    warn_reboot()

    fedora_version = sys.argv[1]
    current_version = get_fedora_version()
    if fedora_version == get_fedora_version() or fedora_version < get_fedora_version():
        print(f"Your current version ({current_version}) is higher than or the same as the target version ({fedora_version}). No update needed.")
        sys.exit(0)
    elif fedora_version == FEDORA_VERSIONS[0]:
        print(f"Fedora {FEDORA_VERSIONS[0]} is the latest stable release.")
        sys.exit(0)

    run_upgrade(fedora_version)    

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
