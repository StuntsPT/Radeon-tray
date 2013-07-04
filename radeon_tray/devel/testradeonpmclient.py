#!/usr/bin/env python

import zmq
import sys

PORT = "5556"

if len(sys.argv) > 1:
    PORT = sys.argv[1]
    int(PORT)

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % PORT)

socket.send("info")

message = socket.recv()

print(message)

socket.send("verifier")

message = socket.recv()

print(message)

socket.send("powerstatus")

message = socket.recv()

print(message)

socket.send("lastpowerstatus")

message = socket.recv()

print(message)

socket.send("setprofile:default")

message = socket.recv()

print(message)

socket.send("setmethod:dynpm")

message = socket.recv()

print(message)