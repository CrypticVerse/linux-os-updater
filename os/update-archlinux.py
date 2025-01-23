#!/bin/python3
import sys
import subprocess
from extra_functions import *

def run_sys_update():
    try:
        print("Running system upgrade...")
        subprocess.run(['sudo', 'pacman', '-Syu'], check=True)
        print("System upgrade completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during pacman operations: {e}. Did you run as root?")
        sys.exit(1)

def main():
    echo_distro("archlinux", version=False)

    run_sys_update()

if __name__ == "__main__":
    main()