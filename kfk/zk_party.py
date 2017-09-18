import time
import threading

from kazoo.client import KazooClient
from kazoo.handlers.threading import SequentialThreadingHandler

hosts = "zookeeper:2181/party"


def join_party():
    handler = SequentialThreadingHandler()
    cli = KazooClient(hosts=hosts, handler=handler)
    cli.start()

    client_id_seq = cli.Counter('/client_id_seq')
    client_id_seq += 1
    client_id = client_id_seq.value
    # print all threads
    for th in threading.enumerate():
        print("%d, %s" % (th.ident if th.ident is not None else -1, th.name))

    ctx = {
        "running": True
    }

    def change_cb(val, znodestat):
        print("value of /running is " + str(val))
        ctx['running'] = val

    cli.create('/running', bytes([1]))
    cli.DataWatch('/running', change_cb)

    party = cli.Party('/workers/test/', client_id)
    party.join()
    while ctx['running']:
        time.sleep(3)
    party.leave()
    cli.stop()


def print_members():
    handler = SequentialThreadingHandler()
    cli = KazooClient(hosts=hosts, handler=handler)
    cli.start()
    party = cli.Party('/workers/test')
    for test in party:
        print(str(test))
    cli.stop()
