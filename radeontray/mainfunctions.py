"""this file contains all main functions
"""
from __future__ import unicode_literals, print_function
from os import path
from getpass import getuser
from .radeonpmserver import server_main
from .radeontrayclient import client_main
from .utils import systemd_path, conf_path, icon_path, paths_verification
import subprocess
import sys

SYSDPATH = systemd_path()
CONFPATH = conf_path()
ICONPATH = icon_path()

def client():
    """Function to start the client and manage the application
    """
    if len(sys.argv) == 1:
        client_main()
    elif sys.argv[1] == "client":
        paths_verification(path.expanduser("~") + "/")
        client_main(client=True)
    elif sys.argv[1] == "install-client":
        if getuser() != "root":
            print("You need root privileges for installation")
            return
        copy_file = "cp %s/radeontrayclient.desktop /usr/share/applications" % CONFPATH
        subprocess.call(copy_file, shell=True)
        subprocess.call("mkdir /usr/share/Radeon-tray-icon", shell=True) 
        copy_file = "cp %s/radeon-tray.svg /usr/share/Radeon-tray-icon" % ICONPATH
        subprocess.call(copy_file, shell=True)
    elif sys.argv[1] == "uninstall-client":
        if getuser() != "root":
            print("You need root privileges to uninstall the application")
            return
        subprocess.call("rm -R /usr/share/Radeon-tray-icon", shell=True)
        subprocess.call("rm /usr/share/applications/radeontrayclient.desktop", shell=True)
    elif sys.argv[1] == "install-client-conf":
        paths_verification(path.expanduser("~") + "/")
    elif sys.argv[1] == "uninstall-client-conf":
        home = path.expanduser("~")
        subprocess.call("rm -R %s/.config/Radeon-tray" % home, shell=True)
    elif sys.argv[1] == "install-server":
        if len(sys.argv) < 3:
            print("Specify the server to install like:\n\t* systemd")
        elif sys.argv[2] == "systemd":
            if getuser() != "root":
                print("You need root privileges for installation")
                return
            copy_file = "cp %s/radeonpm.service /lib/systemd/system" % SYSDPATH
            subprocess.call(copy_file, shell=True)
            subprocess.call("systemctl daemon-reload", shell=True)
            subprocess.call("systemctl start radeonpm.service", shell=True)
            subprocess.call("systemctl enable radeonpm.service", shell=True)
        else:
            print("Command not correct...")
    elif sys.argv[1] == "uninstall-server":
        if len(sys.argv) < 3:
            print("Specify the server to uninstall like:\n\t* systemd")
        elif sys.argv[2] == "systemd":
            if getuser() != "root":
                print("You need root privileges to uninstall the application")
                return
            subprocess.call("systemctl stop radeonpm.service", shell=True)
            subprocess.call("systemctl disable radeonpm.service", shell=True)
            subprocess.call("rm /lib/systemd/system/radeonpm.service", shell=True)
            subprocess.call("systemctl daemon-reload", shell=True)
        else:
            print("Command not correct...")
    else:
            print("Command not correct...")
    

def server():
    """Function to start the server
    """
    if getuser() != "root":
        print("You need root privileges to start the server")
        return
    server_main()
