"""Init module

Copyright 2012-2013 Francisco Pina Martins <f.pinamartins@gmail.com>
and Mirco Tracolli.
This file is part of Radeon-tray.
Radeon-tray is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Radeon-tray is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Radeon-tray.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import unicode_literals, print_function
from os import path
from radeonpmserver import server_main
from radeontrayclient import client_main
from utils import systemd_path, conf_path, icon_path, paths_verification
import subprocess
import sys

__version__ = '1.0'

SYSDPATH = systemd_path()
CONFPATH = conf_path()
ICONPATH = icon_path()

def client():
    """Function to start the client and manage the application
    """
    global SYSDPATH, CONFPATH, ICONPATH
    if len(sys.argv) == 1:
        client_main()
    elif sys.argv[1] == "client":
        paths_verification(path.expanduser("~") + "/")
        client_main(client=True)
    elif sys.argv[1] == "install-server" and\
            sys.argv[2] == "systemd":
        copy_file = "cp %s/radeonpm.service /lib/systemd/system" % SYSDPATH
        subprocess.call(copy_file, shell=True)
        subprocess.call("systemctl daemon-reload", shell=True)
        subprocess.call("systemctl start radeonpm.service", shell=True)
        subprocess.call("systemctl enable radeonpm.service", shell=True)
    elif sys.argv[1] == "uninstall-server"and\
            sys.argv[2] == "systemd":
        subprocess.call("systemctl stop radeonpm.service", shell=True)
        subprocess.call("systemctl disable radeonpm.service", shell=True)
        subprocess.call("rm /lib/systemd/system/radeonpm.service", shell=True)
        subprocess.call("systemctl daemon-reload", shell=True)
    elif sys.argv[1] == "install-client":
        copy_file = "cp %s/radeontrayclient.desktop /usr/share/applications" % CONFPATH
        subprocess.call(copy_file, shell=True)
        subprocess.call("mkdir /usr/share/Radeon-tray-icon", shell=True)
        copy_file = "cp %s/radeon-tray.svg /usr/share/Radeon-tray-icon" % ICONPATH
        subprocess.call(copy_file, shell=True)
    elif sys.argv[1] == "uninstall-client":
        subprocess.call("rm -R /usr/share/Radeon-tray-icon", shell=True)
        subprocess.call("rm /usr/share/applications/radeontrayclient.desktop", shell=True)
    elif sys.argv[1] == "install-client-conf":
        paths_verification(path.expanduser("~") + "/")
    elif sys.argv[1] == "uninstall-client-conf":
        home = path.expanduser("~")
        subprocess.call("rm -R %s/.config/Radeon-tray" % home, shell=True)

def server():
    """Function to start the server
    """
    server_main()