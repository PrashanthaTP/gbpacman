import os
from setuptools import setup, find_packages


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# https://stackoverflow.com/a/54216163/12988588 : dependency links
def get_requirements(req_file):
    with open(req_file, 'r') as file:
        return file.readlines()


setup(
    name="gbpacman",
    version="0.0.1",
    author="Prashantha TP",
    description=("Package Manager for Git Bash"),
    license="MIT",
    keywords="msys2 gitbash bash pacman",
    url="https://github.com/PrashanthaTP/gbpacman",
    packages=find_packages(exclude=['tests']),
    package_data={"gbpacman": ["settings.json",
                               "README.md", "LICENSE", "__version__"]},
    package_dir={"gbpacman": "gbpacman"},
    include_package_data=True,
    install_requires=get_requirements('requirements.txt'),
    python_requires=">=3.7",
    long_description=read_file('README.md'),
    entry_points={
        'console_scripts': ['gbpacman=gbpacman.main:main']
    }
)
