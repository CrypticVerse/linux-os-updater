import sys
import subprocess
import re
import glob

VERSION_TO_NAME = {
    '25.04':'plucky',
    '24.10':'oracular',
}

LATEST_STABLE = '24.10'

def get_current_name():
    try:
        result = subprocess.run(['lsb_release', '-c'], capture_output=True, text=True, check=True)
        match = re.search(r'Codename:\s+(\S+)', result.stdout)
        if match:
            return match.group(1)
        else:
            print("Could not deternime the current version name!")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("error running lsb_release -c")
        sys.exit(1)

def get_current_number():
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

def update_sources(oldName, newName):
    try:
        with open('/etc/apt/sources.list', 'r') as file:
            file_data = file.read()

        # Replace all instances of the old codename with the new one, even in contexts like "focal-security"
        updated_data = re.sub(r'\b' + re.escape(oldName) + r'\b', newName, file_data)

        with open('/etc/apt/sources.list', 'w') as file:
            file.write(updated_data)

        print(f"Replaced {oldName} with {newName} in /etc/apt/sources.list.")
        
        # Optionally, handle other sources list files
        for filename in glob.glob('/etc/apt/sources.list.d/*.list'):
            with open(filename, 'r') as file:
                file_data = file.read()

            updated_data = re.sub(r'\b' + re.escape(oldName) + r'\b', newName, file_data)

            with open(filename, 'w') as file:
                file.write(updated_data)
            print(f"Replaced {oldName} with {newName} in {filename}.")
        
    except PermissionError:
        print("Permission denied. Please run the script as root (sudo).")
        sys.exit(1)
    except FileNotFoundError:
        print("/etc/apt/sources.list file not found.")
        sys.exit(1)

def run_sys_update():
    try:
        print("Running system upgrade...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'full-upgrade', '-y'], check=True)
        subprocess.run(['sudo', 'apt', 'autoremove', '-y'], check=True)
        print("System upgrade completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during apt operations: {e}. Did you run as root?")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: ubuntu-updater <version>")
        sys.exit(1)

    version = sys.argv[1]

    if version == "25.04":
        print(f'Warning: 25.04 (Plucky) is a development release!')
        input("Press Enter to continue, or Ctrl+C to cancel this operation!")

    if version not in VERSION_TO_NAME:
        print(f'Unknown version: {version}')
        sys.exit(1)

    new_name = VERSION_TO_NAME[version]
    current_version = get_current_number()
    current_name = get_current_name()

    if compare(current_version, version) >= 0:
        print(f"Your current version ({current_version}) is higher than or the same as the target version ({version}). No update needed.")
        sys.exit(0)

    # changelog updates soon?
    update_sources(current_name, new_name)

    run_sys_update()

if __name__ == "__main__":
    main()