import argparse


def get_cmd_options():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="Git Bash Package Manager")
    parser.add_argument('-i', '--install', type=str,
                        help="install package from msys package inventory")
    parser.add_argument('--uninstall', type=str,
                        help="uninstall the package from the system if it exists")
    options = parser.parse_args()
    return options
