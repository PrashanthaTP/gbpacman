# gbpacman

![BannerImage](docs/images/gbpacman_banner.png)

Package Manager for Git Bash

## What it does ?

- Lists the available packages with given name
- Downloads and unzips package from msys package repository

## Requirements

- Git bash (latest)
- Python 3.7 and above 

> Note: Tested on Windows 

## Installation

```
pip install --upgrade git+ssh://git@github.com/PrashanthaTP/gbpacman@main
```

## Usage

```bash
usage: gbpacman [-h] [-l LIST] [-i INSTALL] [--uninstall UNINSTALL]

Git Bash Package Manager

optional arguments:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  list packages with given name (default: None)
  -i INSTALL, --install INSTALL
                        install package from msys package inventory (default:
                        None)
  --uninstall UNINSTALL
                        uninstall the package from the system if it exists
                        (default: None)
```

> Note: `--uninstall` not yet implemented.

## Dev

### Todo

- Proper exception handling
- Proper reuse / implementation of parser functions
- Proper reuse / implementation of zip/unzip funcitons
- Proper handling of downloaded,unzipped files
- Maintenance of Settings.json
- Tests improvement
- Implementing '--install-with-url'
- Implementing '--uninstall'
- Improve UI/logging

- Others
  - Is logging really needed to be done through [plogger](https://github.com/PrashanthaTP/plogger)?


# License

MIT
