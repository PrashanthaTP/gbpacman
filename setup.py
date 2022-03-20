import os
from setuptools import setup, find_packages


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="gbpacman",
    version="0.0.1",
    author="Prashantha TP",
    description=("Package Manager for Git Bash"),
    license="MIT",
    keywords="msys2 gitbash bash pacman",
    url="https://github.com/PrashanthaTP/gbpacman",
    packages=find_packages('gbpacman', exclude=['tests']),
    package_dir={"gbpacman": "gbpacman"},
    long_description=read_file('README.md'),
    entry_points={
        'console_scripts': ['gbpacman=gbpacman.main:main']
    }
)
