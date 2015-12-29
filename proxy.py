import zmq
import logging

xpub_url = "tcp://*:7555"
xsub_url = "tcp://*:7556"
mon_url = "tcp://*:7557"

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

if __name__ == '__main__':
    ctx = zmq.Context()
    xpub = ctx.socket(zmq.XPUB)
    xpub.bind(xpub_url)
    logging.info('XPUB socket bind to address %s', xpub_url)
    xsub = ctx.socket(zmq.XSUB)
    xsub.bind(xsub_url)
    logging.info('XSUB socket bind to address %s', xsub_url)
    push = ctx.socket(zmq.PUSH)
    push.bind(mon_url)
    logging.info('Monitor socket bind to address %s', mon_url)
    try:
        zmq.proxy(xpub, xsub, push)
    except KeyboardInterrupt:
        print('You pressed Ctrl+C! Shutting down')
        ctx.destroy(linger=1)
