import zmq, logging, threading, sched, json, time

xpub_url = "tcp://*:7555"
xsub_url = "tcp://*:7556"
mon_url = "tcp://*:7557"

s = sched.scheduler(time.time, time.sleep)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


def proxy(ctx):
    xpub = ctx.socket(zmq.XPUB)
    xpub.bind(xpub_url)
    logging.info('XPUB socket bind to address %s', xpub_url)
    xsub = ctx.socket(zmq.XSUB)
    xsub.bind(xsub_url)
    logging.info('XSUB socket bind to address %s', xsub_url)
    push = ctx.socket(zmq.PUSH)
    push.bind(mon_url)
    logging.info('Monitor socket bind to address %s', mon_url)
    zmq.proxy(xpub, xsub, push)


def mon(ctx):
    pull = ctx.socket(zmq.PULL)
    pull.connect("tcp://127.0.0.1:7557")
    while True:
        msg = pull.recv();
        logging.info('Recived %s', msg)


def health_check_job(sc, socket):
    socket.send_multipart([b'health_check', bytes(json.dumps({'type': 'health_check', 'id': 'proxy'}), 'utf8')])
    sc.enter(1, 1, health_check_job, (sc, socket))


def add_health_check(ctx):
    health_check_socket = ctx.socket(zmq.PUB)
    health_check_socket.connect('tcp://127.0.0.1:7556')
    s.enter(1, 1, health_check_job, (s, health_check_socket))


if __name__ == '__main__':
    ctx = zmq.Context()
    proxy = threading.Thread(target=proxy, args=(ctx,))
    proxy.start()
    mon = threading.Thread(target=mon, args=(ctx,))
    mon.start()
    add_health_check(ctx)

    try:
        s.run()
    except KeyboardInterrupt:
        print('You pressed Ctrl+C! Shutting down')
        ctx.destroy(linger=1)
