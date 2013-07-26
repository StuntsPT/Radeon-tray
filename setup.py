#!/usr/bin/env python

from setuptools import setup
import glob
import radeontray
import os
import sys

SCRIPTS = glob.glob("scripts/*")
ASSETS = glob.glob('radeontray/assets/*')
DATA_FILES = [('/usr/share/Radeon-tray-pixmaps', ASSETS)]

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
 
DATA_FILES.append(('/lib/systemd/system', ['radeontray/systemd/radeonpm.service']))
DATA_FILES.append(('/usr/share/applications', ['radeontray/conf/radeontrayclient.desktop']))

setup(
    name='Radeon-tray',
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
    install_requires=['pyzmq>=13.1.0'],
    packages=['radeontray'],
    package_data={'radeontray': ['assets/*.svg', 'devel/*.py', 'systemd/*.service']
    },
    scripts=SCRIPTS,
    data_files=DATA_FILES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)