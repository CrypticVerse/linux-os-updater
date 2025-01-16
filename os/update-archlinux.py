import sys
import subprocess

def run_sys_update():
    try:
        print("Running system upgrade...")
        subprocess.run(['sudo', 'pacman', '-Syu'], check=True)
        print("System upgrade completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during pacman operations: {e}. Did you run as root?")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: archlinux-updater <version>")
        sys.exit(1)

    run_sys_update()

if __name__ == "__main__":
    main()