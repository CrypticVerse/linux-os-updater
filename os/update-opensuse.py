#!/bin/python3
import sys
import subprocess
import re
from extra_functions import *

def new_python(current_version):
    try:
        subprocess.run(f"zypper addrepo https://download.opensuse.org/repositories/devel:languages:python:Factory/{current_version}/devel:languages:python:Factory.repo", shell=True, check=True)
        subprocess.run("zypper refresh", shell=True, check=True)
        subprocess.run("zypper install python310", shell=True, check=True)
        subprocess.run("sudo update-alternatives --set python3 /usr/bin/python3.10", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Error running zypper.")
        sys.exit(1)

def edit_keys():
    try:
        subprocess.run("rpm --import /usr/lib/rpm/gnupg/keys/gpg-pubkey-29b700a4-62b07e22.asc", shell=True, check=True)
        subprocess.run("rpm --import /usr/lib/rpm/gnupg/keys/gpg-pubkey-25db7ae0-645bae34.asc", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Error running rpm.")
        sys.exit(1) 


def get_suse_version():
    try:
        result = subprocess.run(['lsb_release', '-r'], capture_output=True, text=True, check=True)
        try:
            subprocess.run(['lsb_release', '--version'], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
            subprocess.run("sudo zypper install -y lsb-release", shell=True, check=True)
            result = subprocess.run(['lsb_release', '-r'], capture_output=True, text=True, check=True)
        match = re.search(r'Release:\s+(\S+)', result.stdout)
        if match:
            return match.group(1)
        else:
            print("Could not determine the current openSUSE version.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error running lsb_release.")
        sys.exit(1)

def runUpdate(new_version):
    suse_version = get_suse_version()
    try:
        subprocess.run("sudo zypper refresh && sudo zypper update", shell=True, check=True)
        subprocess.run(f"sed -i 's/${suse_version}/${new_version}/g' /etc/zypp/repos.d/*", shell=True, check=True)
        subprocess.run(f"sudo zypper --releasever={new_version} refresh", shell=True, check=True)
        subprocess.run(f"sudo zypper --releasever={new_version} dup", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Error running zypper.")
        sys.exit(1)  

def main():
    echo_distro("opensuse", version=True)

    current_python_version = sys.version_info
    if current_python_version < (3, 10):
        new_python(get_suse_version())

    suse_version = get_suse_version()
    new_suse_version = sys.argv[1]

    warn_reboot()

    if suse_version == '15.4':
        edit_keys()

    sorted_versions = sorted(SUSE_VERSIONS, key=lambda x: list(map(int, x.split('.'))))    

    if suse_version == sorted_versions[0]:
        print("You are already on the latest version of openSUSE.")
        sys.exit(1)
    elif suse_version <= '15.2':
        print("Upgrading from openSUSE 15.2 or lower is unsupported. Please follow the guide on the openSUSE website.")    
        sys.exit(1)
    elif new_suse_version >= '16.0':
        print("Upgrading to openSUSE 16.0 or higher is currently unsupported. Please follow the guide on the openSUSE website.")    
        sys.exit(1)

    runUpdate(new_suse_version)
    subprocess.run("sudo reboot", shell=True, check=True)

if __name__ == '__main__':
    main()
