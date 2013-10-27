#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Server module


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
import zmq
from .utils import power_method_set, \
    power_profile_set, \
    power_status_get, \
    radeon_info_get, \
    verifier

PORT = "5556"
CARDS = verifier()


def server_main(port=False):
    """Main function of the server
    """
    global PORT, CARDS

    #Main function
    init_method, init_profile = power_status_get().split(",")
    #Default values
    def_method, def_profile = ["dynpm", "default"]

    # Apply the last configuration if it differs from default
    if def_method != init_method or def_profile != init_profile:
        power_profile_set(def_profile, CARDS)
        power_method_set(def_method, CARDS)

    if port:
        PORT = port
    int(PORT)

    CONTEXT = zmq.Context()
    SOCKET = CONTEXT.socket(zmq.REP)
    SOCKET.bind("tcp://*:%s" % PORT)

    while True:
        message = SOCKET.recv_string()

        if message == "info":
            SOCKET.send_string(radeon_info_get())
        elif message == "verifier":
            SOCKET.send_string(str(verifier()))
        elif message == "powerstatus":
            SOCKET.send_string(power_status_get())
        elif message.find(":"):
            try:
                command, arg, user_home = message.split(":")
            except ValueError:
                SOCKET.send_string("Command not correct")
            if command == "setprofile":
                power_profile_set(arg, CARDS, home=user_home)
                SOCKET.send_string("True")
            elif command == "setmethod":
                power_method_set(arg, CARDS, home=user_home)
                SOCKET.send_string("True")
            else:
                SOCKET.send_string("Command not found")
        else:
            SOCKET.send_string("Command not found")