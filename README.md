# Linux OS Updater

Linux OS Updater is a Python tool designed to simplify the process of updating and upgrading your Linux based operating system. This tool automates the steps required to keep your system up-to-date with the latest packages.

## Features

- Imitate do-release-upgrade on Debian-based systems
- Update package lists
- Upgrade installed packages
- Clean up unnecessary packages

## Requirements

- Python 3.x

## Installation

Install can be done with Snap by Canoical.
Python is included in the snap dependencies.

```sh
sudo snap install linux-os-updater
```

If your linux OS is unsupported by snap, or the snap does not work, run the dedicated bash script.
Python must also be installed before hand.
```bash
curl -fsSL https://raw.githubusercontent.com/CrypticVerse/linux-os-updater/refs/heads/master/install.sh | bash
```

## Usage

To update your Linux-based OS, run
```sh
sudo update-<distro> [optional<version>]
```
The version arg is optional or required based on the list specified [here](https://github.com/CrypticVerse/linux-os-updater/wiki/command-args)

If you find that it says unknown version when specifying a version number, but that version exists, you can run this to update the scripts.
```bash
sudo update-os-updater
```

## Bugs

For any questions or suggestions, please open an issue.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.