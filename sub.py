import sys
import zmq

port = "7555"
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect ("tcp://127.0.0.1:%s" % port)

socket.setsockopt_string(zmq.SUBSCRIBE, "sensor")
socket.setsockopt_string(zmq.SUBSCRIBE, "health_check")

while True:
    topic, messagedata = socket.recv_multipart()
    print(topic, messagedata)
