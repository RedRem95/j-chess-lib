#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from setuptools.command import build_py


class BuildExtension(build_py.build_py):

    def run(self):
        import os
        xsd_url = os.environ.get("j-chess-xsd-url", "https://raw.githubusercontent.com/JoKrus/j-chess-xsd/master/jChessMessage.xsd")
        os.system("rm -rf j_chess_lib/communication/schema")
        print("Removed old schema data")
        os.system("xsdata %s --package j_chess_lib.communication.schema" % xsd_url)
        print("Installed new schema data")


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

test_requirements = []

setup(
    author="Alexander Vollmer",
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python library for a j-chess bot. Beep Boop",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='j_chess_lib',
    name='j_chess_lib',
    packages=find_packages(include=['j_chess_lib', 'j_chess_lib.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/RedRem95/j_chess_lib',
    version='0.1.0',
    zip_safe=False,
    cmdclass={
        'build_py': BuildExtension,
    },
)
