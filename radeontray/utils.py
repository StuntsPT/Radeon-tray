#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, makedirs
import sys

PROFILE_PATH = ".config/Radeon-tray/last_power_profile"
METHOD_PATH = ".config/Radeon-tray/last_power_method"

def verifier(client=None):
    #First we verify how many cards we are dealing with, if any. Quit if none
    #are found.
    if client is not None:
        client.send("verifier")
        message = client.recv()
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
        client.send("info")
        message = client.recv()
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
        client.send("powerstatus")
        message = client.recv()
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
        client.send("setprofile:"+new_power_profile+":"+home)
        message = client.recv()
        return bool(message)
    else:
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
        client.send("setmethod:"+new_power_method+":"+home)
        message = client.recv()
        return bool(message)
    else:
        try:
            for i in range(cards):
                with open("/sys/class/drm/card"+str(i)+"/device/power_method","w") as f:
                    f.write(new_power_method)
            with open(home + METHOD_PATH, "w") as fs:
                fs.write(new_power_method)
        except IOError:
            return False
        return True

def paths_verification():
    config_location = path.dirname(PROFILE_PATH)
    if path.isdir(config_location) == False:
        makedirs(config_location)
        with open(METHOD_PATH, "w") as f:
            f.write("profile")
        with open(PROFILE_PATH, "w") as f:
            f.write("default")
        print("Warning: configuration path not found for this user. Created a new one here:%s\n" % (config_location))
    elif path.isfile(PROFILE_PATH) == False or path.isfile(METHOD_PATH) == False:
        with open(METHOD_PATH, "w") as f:
            f.write("profile")
        with open(PROFILE_PATH, "w") as f:
            f.write("default")
        print("Warning: configuration files not found for this user (but path exists). Created a new ones here:%s\n" % (config_location))

paths_verification()