import os
from setuptools import setup, find_packages


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = ['plogger']
dependency_links = [
    "plogger @ git+https://github.com/PrashanthaTP/plogger.git@main#egg=plogger-0.0.1"]
setup(
    name="gbpacman",
    version="0.0.1",
    author="Prashantha TP",
    description=("Package Manager for Git Bash"),
    license="MIT",
    keywords="msys2 gitbash bash pacman",
    url="https://github.com/PrashanthaTP/gbpacman",
    packages=find_packages(exclude=['tests']),
    package_dir={"gbpacman": "gbpacman"},
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    long_description=read_file('README.md'),
    entry_points={
        'console_scripts': ['gbpacman=gbpacman.main:main']
    }
)
