import zmq
import random
import time
import json
from random import choice

port = "7556"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://127.0.0.1:%s" % port)
while True:
    topic = bytes('sensor', 'UTF8')
    messages = ['Salary', 'Queen', 'Once', 'Fry', 'Mud', 'Thus', 'Effort', 'Elastic', 'Produce', 'Cake']
    msg = bytes(json.dumps({'message': choice(messages)}), 'UTF8')
    print("%s %s" % (topic, msg))
    socket.send_multipart([topic, msg])
    time.sleep(1)
