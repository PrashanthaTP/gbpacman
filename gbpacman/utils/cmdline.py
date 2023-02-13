import argparse


def get_cmd_options(settings):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=f"Git Bash Package Manager ({settings['VERSION']})")
    parser.add_argument('-l', '--list', type=str,
                        help="list packages with given name")
    parser.add_argument('-i', '--install', type=str,
                        help="install package from msys package inventory")
    parser.add_argument('-u', '--install-from-url', type=str,
                        help="install package given zip file url")
    parser.add_argument('--uninstall', type=str,
                        help="uninstall the package from the system if it exists")
    options = parser.parse_args()
    return options
