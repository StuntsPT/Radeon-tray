#!/usr/bin/python

from setuptools import setup
import glob

setup(name='Radeon-tray', packages=['radeon_tray'],
description='A small program to control the power profiles of your Radeon card via systray icon.',
url='https://github.com/StuntsPT/Radeon-tray', install_requires=['PyQt>=4.0'],
data_files=[('share/pixmaps', glob.glob('radeon_tray/assets/*')), ('lib/systemd/system', ['radeon_tray/systemd/radeonpm.service']),
('bin', ['radeon_tray/bin/Radeon-tray.py']), ('sbin', ['radeon_tray/bin/radeonpmserver.py'])])