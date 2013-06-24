#!/usr/bin/python
# -*- coding: utf-8 -*-
import zmq
import sys
from os import path

PORT = "5556"
PROFILE_PATH = path.join(path.dirname(__file__), "last_power_profile")
METHOD_PATH = path.join(path.dirname(__file__), "last_power_method")

def verifier():
    #First we verify how many cards we are dealing with, if any. Quit if none
    #are found.
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
    """Tests a few paths for card temperatur
    """
    paths_list = ["/sys/class/drm/card0/device/hwmon/hwmon1/temp1_input"]
    temp_path = ""
    for tpath in paths_list:
        if path.exists(tpath):
            temp_path = tpath
    
    return temp_path

def temp_checker(temp_path):
    if temp_path == "":
        return "No temperature info"
    with open(temp_path, "r") as f:
        temperature = f.read()
    temp = str(int(temperature) / 1000) + "°C"
    return temp


def radeon_info_get():
    """Get the power info
    """
    cards = verifier()
    radeon_info = ""
    for xc in range(cards):
        radeon_info += "----- Card%d -----\n" % xc
        psg = power_status_get(xc).split(",")
        radeon_info += "Power method: %s\nPower profile: %s\n" % (psg[0], psg[1])
        radeon_info += temp_checker(temp_location()) + "\n"
        with open("/sys/kernel/debug/dri/"+str(xc)+"/radeon_pm_info","r") as f:
            radeon_info += f.read().strip()
        radeon_info += "\n---------------"
    return radeon_info


def power_status_get(num=0):
    """Get the power status. Uses with to close the file immediatelly
    """
    with open("/sys/class/drm/card"+str(num)+"/device/power_method","r") as f:
        power_method = f.readline().strip()
    with open("/sys/class/drm/card"+str(num)+"/device/power_profile","r") as f:
        power_profile = f.readline().strip()
    return power_method+","+power_profile

def last_power_status_get():
    """Get the last power status
    """
    with open(METHOD_PATH, "r") as f:
        power_method = f.readline().strip()
    with open(PROFILE_PATH, "r") as f:
        power_profile = f.readline().strip()
    return power_method+","+power_profile

def power_profile_set(new_power_profile, cards):
    """Change the power profile
    """
    for i in range(cards):
        with open("/sys/class/drm/card"+str(i)+"/device/power_profile","w") as f:
            f.write(new_power_profile)
    with open(PROFILE_PATH, "w") as fs:
        fs.write(new_power_profile)

def power_method_set(new_power_method, cards):
    """Change the power method
    """
    for i in range(cards):
        with open("/sys/class/drm/card"+str(i)+"/device/power_method","w") as f:
            f.write(new_power_method)
    with open(METHOD_PATH, "w") as fs:
        fs.write(new_power_method)

CARDS = verifier()

if __name__ == '__main__':
    
    #Main function
    init_method, init_profile = power_status_get().split(",")
    l_method, l_profile = last_power_status_get().split(",")
    
    # Check if is lost the last configuration
    if l_method != init_method or l_profile != init_profile:
        power_profile_set(l_profile, CARDS)
        power_method_set(l_method, CARDS)
    
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    int(PORT)
    
    CONTEXT = zmq.Context()
    SOCKET = CONTEXT.socket(zmq.REP)
    SOCKET.bind("tcp://*:%s" % PORT)

    while True:
        message = SOCKET.recv()
        
        if message == "info":
            SOCKET.send(radeon_info_get())
        elif message == "verifier":
            SOCKET.send(str(verifier()))
        elif message == "powerstatus":
            SOCKET.send(power_status_get())
        elif message == "lastpowerstatus":
            SOCKET.send(last_power_status_get())
        elif message.find(":"):
            try:
                command, arg = message.split(":")
            except ValueError:
                SOCKET.send("Command not correct")
            if command == "setprofile":
                power_profile_set(arg, CARDS)
                SOCKET.send("True")
            elif command == "setmethod":
                power_method_set(arg, CARDS)
                SOCKET.send("True")
            else:
                SOCKET.send("Command not found")
        else:
            SOCKET.send("Command not found")