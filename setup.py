#!/usr/bin/env python
"""Installer for radeontray program
"""
from setuptools import setup
import radeontray
import os

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='Radeon-tray',
    zip_safe=False,
    #Include data from MANIFEST.in
    #include_package_data = True,
    version=radeontray.__version__,
    author="Pina Martins",
    author_email='f.pinamartins@gmail.com',
    # To add
    #long_description=read('README'),
    description='A small program to control the power profiles of your Radeon card via systray icon.',
    url='https://github.com/StuntsPT/Radeon-tray',
    license="GPLv3",
    keywords = "radeon tray icon",
    setup_requires=['pyzmq>=13.1.0'],
    dependency_links = ['http://sourceforge.net/projects/pyqt/files/latest/download?source=files'],
    packages=['radeontray'],
    package_data={'radeontray':
        ['assets/*.svg', 'devel/*.py', 'systemd/*.service', 'conf/*.desktop']
    },
    #scripts=SCRIPTS,
    #data_files=DATA_FILES,
    entry_points={
        'console_scripts': [
            'radeontray = radeontray:client',
            'radeontrayserver = radeontray:server'
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)