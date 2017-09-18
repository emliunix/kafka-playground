"""
"""
import time
import threading

from kafka import (
    KafkaConsumer,
    KafkaProducer,
    TopicPartition,
)


bootstrap_servers = ["kafka:9092"]

p = KafkaProducer(bootstrap_servers=bootstrap_servers,
                  client_id="test_producer")


class Producer(threading.Thread):
    def run(self):
        while True:
            p.send('hello', value=b"Hello")
            p.flush()
            print('sent')
            time.sleep(1)


class Consumer(threading.Thread):
    def run(self):
        c = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                          client_id="test_consumer",
                          group_id="consume_hello")
        c.subscribe(topics=("hello",))
        while True:
            msgs = c.poll(timeout_ms=3000)
            if msgs:
                self.process_msgs(msgs)
            time.sleep(2)
            for part_id in c.partitions_for_topic("hello"):
                tp = TopicPartition("hello", part_id)
                position = c.position(tp) or 0
                highwater = c.highwater(tp) or 0
                print("%s:%d %d/%d" % ("hello", part_id, position, highwater))

    def process_msgs(self, msgs):
        pass


Producer().start()
Consumer().start()
