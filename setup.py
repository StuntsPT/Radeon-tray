#!/usr/bin/env python

from setuptools import setup
import glob

scripts = ['Radeon-tray.py', 'radeonpmserver.py']


setup(name='Radeon-tray', packages=['radeon_tray'],
description='A small program to control the power profiles of your Radeon card via systray icon.',
url='https://github.com/StuntsPT/Radeon-tray', install_requires=['PyQt>=4.0'],
scripts=['scripts/' + x for x in scripts],
data_files=[('share/pixmaps', glob.glob('radeon_tray/assets/*')),
('lib/systemd/system', ['radeon_tray/systemd/radeonpm.service'])])