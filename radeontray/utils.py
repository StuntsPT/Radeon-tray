#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utils for radeontray program

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
from os import path, makedirs
import sys

PROFILE_PATH = ".config/Radeon-tray/last_power_profile"
METHOD_PATH = ".config/Radeon-tray/last_power_method"

def icon_path():
    return path.abspath(path.join(path.dirname(__file__), "assets"))

def systemd_path():
    return path.abspath(path.join(path.dirname(__file__), "systemd"))

def conf_path():
    return path.abspath(path.join(path.dirname(__file__), "conf"))

def verifier(client=None):
    #First we verify how many cards we are dealing with, if any. Quit if none
    #are found.
    if client is not None:
        client.send_string("verifier")
        message = client.recv_string()
        return int(message)
    else:
        cards = 0
        if path.isdir("/sys/class/drm/card0"):
            cards += 1
        if path.isdir("/sys/class/drm/card1"):
            cards += 1
        if cards == 0:
            sys.exit("No suitable cards found.\nAre you using the OSS Radeon \
    drivers?\nExiting the program.")
        return cards

def temp_location():
    """Tests a few paths for card temperature
    """
    paths_list = ["/sys/class/drm/card0/device/hwmon/hwmon1/temp1_input"]
    temp_path = ""
    for tpath in paths_list:
        if path.exists(tpath):
            temp_path = tpath

    return temp_path

def temp_checker(temp_path):
    """Check the card temperature in sysfs, if a suitable entry was found
    """
    if temp_path == "":
        return "No temperature info"
    with open(temp_path, "r") as f:
        temperature = f.read()
    temp = str(int(temperature) / 1000) + "°C"
    return temp

def radeon_info_get(client=None):
    """Get the power info
    """
    if client is not None:
        client.send_string("info")
        message = client.recv_string()
        return message
    else:
        cards = verifier()
        radeon_info = ""
        for xc in range(cards):
            radeon_info += "----- Card%d -----\n" % xc
            method, profile = power_status_get(xc).split(",")
            radeon_info += "Power method: %s\nPower profile: %s\n" % (method, profile)
            radeon_info += temp_checker(temp_location()) + "\n"
            try:
                with open("/sys/kernel/debug/dri/"+str(xc)+"/radeon_pm_info","r") as ff:
                    radeon_info += ff.read().strip()
            except IOError:
                radeon_info += "\nYou need root privileges\nfor more information"
            radeon_info += "\n---------------"
        return radeon_info


def power_status_get(num=0, client=None):
    """Get the power status. Uses with to close the file immediatelly
    """
    if client is not None:
        client.send_string("powerstatus")
        message = client.recv_string()
        return message
    else:
        with open("/sys/class/drm/card"+str(num)+"/device/power_method","r") as f:
            power_method = f.readline().strip()
        with open("/sys/class/drm/card"+str(num)+"/device/power_profile","r") as f:
            power_profile = f.readline().strip()
        return power_method+","+power_profile

def last_power_status_get(home):
    """Get the last power status
    """
    #Try if ther's no file configuration
    try:
        with open(home + METHOD_PATH, "r") as f:
            power_method = f.readline().strip()
        with open(home + PROFILE_PATH, "r") as f:
            power_profile = f.readline().strip()
    except IOError:
        makedirs(home + "/".join(METHOD_PATH.split("/")[:-1]))
        with open(home + METHOD_PATH, "w") as f:
            f.write("default")
        with open(home + PROFILE_PATH, "w") as f:
            f.write("dynpm")
        return "default,dynpm"
    return power_method+","+power_profile

def power_profile_set(new_power_profile, cards, home=None, client=None):
    """Change the power profile
    """
    if client is not None:
        client.send_string("setprofile:"+new_power_profile+":"+home)
        message = client.recv_string()
        return bool(message)
    else:
        if home is not None:
            try:
                for i in range(cards):
                    with open("/sys/class/drm/card"+str(i)+"/device/power_profile","w") as f:
                        f.write(new_power_profile)
                with open(home + PROFILE_PATH, "w") as fs:
                    fs.write(new_power_profile)
            except IOError:
                return False
        return True


def power_method_set(new_power_method, cards, home=None, client=None):
    """Change the power method
    """
    if client is not None:
        client.send_string("setmethod:"+new_power_method+":"+home)
        message = client.recv_string()
        return bool(message)
    else:
        if home is not None:
            try:
                for i in range(cards):
                    with open("/sys/class/drm/card"+str(i)+"/device/power_method","w") as f:
                        f.write(new_power_method)
                with open(home + METHOD_PATH, "w") as fs:
                    fs.write(new_power_method)
            except IOError:
                return False
        return True

def paths_verification(home):
    config_location = path.dirname(home + PROFILE_PATH)
    if path.isdir(config_location) == False:
        makedirs(config_location)
        with open(home + METHOD_PATH, "w") as f:
            f.write("default")
        with open(home + PROFILE_PATH, "w") as f:
            f.write("dynpm")
        print("Warning: configuration path not found for this user. Created a new one here:%s\n" % (config_location))
    elif path.isfile(home + PROFILE_PATH) == False or path.isfile(home + METHOD_PATH) == False:
        with open(home + METHOD_PATH, "w") as f:
            f.write("default")
        with open(home + PROFILE_PATH, "w") as f:
            f.write("dynpm")
        print("Warning: configuration files not found for this user (but path exists). Created a new ones here:%s\n" % (config_location))