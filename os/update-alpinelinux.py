#!/bin/python3
import sys
import subprocess

def warn_reboot():
    print(f"\033[33mWarning: This program WILL reboot your system. Are you sure you want to continue?\033[0m")
    choice = input("continue? [y/N] ").strip().lower()
    if choice in ['n', 'no']:
        print("exiting...")
        sys.exit(1)

def get_os_version():
    with open("/etc/os-release") as f:
        for line in f:
            if line.startswith("VERSION_ID"):
                version_id = line.split("=")[1].strip().strip('"')
                major_minor_version = ".".join(version_id.split(".")[:2])
                return major_minor_version
    return None

def normal_upgrade(new_version):
    warn_reboot()
    try:
        print("Running system upgrade...")
        version = get_os_version()
        
        subprocess.run("setup-apkrepos", shell=True, check=True)
        current_major, current_minor = version.split(".")
        new_major, new_minor = new_version.split(".")
        subprocess.run(f"sed -i -e 's/v{current_major}\\.{current_minor}/v{new_major}\\.{new_minor}/g' /etc/apk/repositories", shell=True, check=True)
        subprocess.run("apk update && apk add --upgrade apk-tools && apk upgrade --available", shell=True, check=True)
        subprocess.run("sync && reboot", shell=True, check=True)

        print("System upgrade completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during apk operations: {e}. Did you run as root?")
        sys.exit(1)

def edge_upgrade():
    version = get_os_version()
    subprocess.run("setup-apkrepos", shell=True, check=True)
    current_major, current_minor = version.split(".")
    subprocess.run(f"sed -i -e 's/v{current_major}\\.{current_minor}/edge/g' /etc/apk/repositories", shell=True, check=True)
    subprocess.run("apk update && apk add --upgrade apk-tools && apk upgrade --available", shell=True, check=True)
    subprocess.run("sync && reboot", shell=True, check=True)    

def main():
    if len(sys.argv) != 2 or sys.argv[2] not in ["--edge", "-e"]:
        print("Usage: update-alpinelinux [<version>|edge]")
        sys.exit(1)

    new_alpine_version = sys.argv[1]

    if new_alpine_version == "edge":
        edge_upgrade()
    else:
        normal_upgrade(new_alpine_version)    

if __name__ == "__main__":
    main()        