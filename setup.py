#!/usr/bin/python

from setuptools import setup

setup(name='Radeon-tray', packages=['radeon-tray'],
description='A small program to control the power profiles of your Radeon card via systray icon.',
url='https://github.com/StuntsPT/Radeon-tray', install_requires=['PyQt>=4.0'],
data_files=[('assets', ['assets/*']), ('/lib/systemd/system', ['systemd/radeonpm.service']),
('/usr/bin', ['bin/Radeon-tray.py']), ('/usr/sbin', ['bin/radeonpmserver.py'])])