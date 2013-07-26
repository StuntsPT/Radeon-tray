#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
import sys
from radeontray.utils import power_method_set, \
    power_profile_set, \
    power_status_get, \
    radeon_info_get, \
    verifier

PORT = "5556"
CARDS = verifier()

if __name__ == '__main__':

    #Main function
    init_method, init_profile = power_status_get().split(",")
    #Default values
    def_method, def_profile = ["default", "dynpm"]

    # Apply the last configuration if it differs from default
    if def_method != init_method or def_profile != init_profile:
        power_profile_set(def_profile, CARDS)
        power_method_set(def_method, CARDS)

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
        elif message.find(":"):
            try:
                command, arg, user_home = message.split(":")
            except ValueError:
                SOCKET.send("Command not correct")
            if command == "setprofile":
                power_profile_set(arg, CARDS, home=user_home)
                SOCKET.send("True")
            elif command == "setmethod":
                power_method_set(arg, CARDS, home=user_home)
                SOCKET.send("True")
            else:
                SOCKET.send("Command not found")
        else:
            SOCKET.send("Command not found")