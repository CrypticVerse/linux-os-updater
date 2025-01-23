import sys

UBUNTU_VERSION_TO_NAME = {
    # Ubuntu
    '24.10':'oracular',
    '24.04':'jammy',
    '23.10':'mantic',
    '23.04':'lunar',
    '22.10':'kinetic',
    '22.04':'jammy',
    '21.10':'impish',
    '21.04':'hirsute',
    '20.10':'groovy',
    '20.04':'focal',
    '19.10':'eoan',
    '19.04':'disco',
    '18.10':'cosmic',
    '18.04':'bionic',
    '17.10':'artful',
    '17.04':'zesty',
    '16.10':'yakkety',
    '16.04':'xenial',
    '15.10':'wily',
    '15.04':'vivid',
    '14.10':'utopic',
    '14.04':'trusty',
    '13.10':'saucy',
    '13.04':'raring',
    '12.10':'quantal',
    '12.04':'precise',
    '11.10':'oneiric',
    '11.04':'natty',
    '10.10':'maverick',
    '10.04':'lucid',
    '9.10':'karmic',
    '9.04':'jaunty',
    '8.10':'intrepid',
    '8.04':'hardy',
    '7.10':'gutsy',
    '7.04':'feisty',
    '6.10':'edgy',
    '6.06':'dapper',
    '5.10':'breezy',
    '5.04':'hoary',
    '4.10':'warty',
}
LINUXMINT_VERSIONS_TO_NAME = {
    '22.1': 'xia',
    '22': 'wilma',
    '21.3': 'virginia',
    '21.2': 'victoria',
    '21.1': 'vera',
    '21': 'vanessa',
    '20.3': 'una',
    '20.2': 'uma',
    '20.1': 'ulyssa',
    '20': 'ulyana',
    '6': 'faye',
}

SUSE_VERSIONS = {
    '16',
    '15.6',
    '15.5',
    '15.4',
    '15.3',
}

FEDORA_VERSIONS_UNSORTED = {str(i) for i in range(41, 0, -1)}
FEDORA_VERSIONS = sorted(FEDORA_VERSIONS_UNSORTED, reverse=True, key=int)

def warn_reboot():
    print(f"\033[33mWarning: This program WILL reboot your system. Are you sure you want to continue?\033[0m")
    choice = input("continue? [y/N] ").strip().lower()
    if choice in ['n', 'no']:
        print("exiting...")
        sys.exit(1)

def echo_distro(distro, version: bool = False):
    if version == False:
        if len(sys.argv) != 1:
            print(f"Usage: update-{distro}")
            sys.exit(1)
    else:
        if len(sys.argv) != 2:
            print(f"Usage: update-{distro} <version>")
            sys.exit(1)
