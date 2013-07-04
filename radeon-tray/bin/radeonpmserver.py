#!/usr/bin/python
# -*- coding: utf-8 -*-
import zmq
import sys
from utils import last_power_status_get, \
    power_method_set, \
    power_profile_set, \
    power_status_get, \
    radeon_info_get, \
    verifier

PORT = "5556"
CARDS = verifier()

if __name__ == '__main__':

    #Main function
    init_method, init_profile = power_status_get().split(",")
    l_method, l_profile = last_power_status_get().split(",")

    # Apply the last configuration if it differs from default
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