import zmq
import random
import sys
import time

port = "7557"
ctx = zmq.Context()
socket = ctx.socket(zmq.PULL)
socket.connect("tcp://127.0.0.1:%s" % port)
try:
    while True:
        string = socket.recv();
        print(string)
except KeyboardInterrupt:
    print('You pressed Ctrl+C! Shutting down')
    ctx.destroy(linger=1)

