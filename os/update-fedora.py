import os
import sys
import re
import subprocess

LATEST_STABLE = '41'

def get_fedora_version():
    try:
        result = subprocess.run(['lsb_release', '-r'], capture_output=True, text=True, check=True)
        match = re.search(r'Release:\s+(\S+)', result.stdout)
        if match:
            return match.group(1)
        else:
            print("Could not determine the current Ubuntu version.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error running lsb_release.")
        sys.exit(1)

def run_upgrade_and_reboot(version):
    print("Upgrading the system...")
    subprocess.run(['sudo', 'dnf', 'upgrade', '--refresh', '-y'], check=True)
    
    script_content = f"""#!/bin/bash
    # This script runs after reboot to start the system upgrade
    sudo dnf system-upgrade download --releasever={version} -y
    """
    
    # Write the script to /usr/local/bin/run_upgrade_after_reboot.sh
    script_path = '/usr/local/bin/run_upgrade_after_reboot.sh'
    with open(script_path, 'w') as f:
        f.write(script_content)

    # Make the script executable
    os.chmod(script_path, 0o755)
    
    # Step 3: Create a systemd service to run the script after reboot
    service_content = f"""[Unit]
    Description=Run dnf system-upgrade after reboot
    After=network.target

    [Service]
    Type=oneshot
    ExecStart={script_path}
    RemainAfterExit=true

    [Install]
    WantedBy=multi-user.target
    """
    
    # Write the systemd service file
    service_path = '/etc/systemd/system/run_upgrade_after_reboot.service'
    with open(service_path, 'w') as f:
        f.write(service_content)

    # Reload systemd and enable the service
    print("Creating systemd service to run after reboot...")
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
    subprocess.run(['sudo', 'systemctl', 'enable', 'run_upgrade_after_reboot.service'], check=True)
    
    # Step 4: Reboot the system
    print("Rebooting the system...")
    subprocess.run(['sudo', 'reboot'])

def main():
    if len(sys.argv) != 2:
        print("Usage: update-fedora <version>")
        sys.exit(1)

    fedora_version = sys.argv[1]
    current_version = get_fedora_version()
    if fedora_version == get_fedora_version() or fedora_version < get_fedora_version():
        print(f"Your current version ({current_version}) is higher than or the same as the target version ({fedora_version}). No update needed.")
        sys.exit(0)
    elif fedora_version == LATEST_STABLE:
        print("Fedora 41 is the latest stable release.")
        sys.exit(0)
    elif fedora_version == LATEST_STABLE + 1:
        print("Fedora 42 is a development release!")
        input("Press Enter to continue, or Ctrl+C to cancel this operation.")    

    run_upgrade_and_reboot(fedora_version)    

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
