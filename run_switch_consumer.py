import time
import itertools
import threading

from kafka import KafkaConsumer, TopicPartition

WAIT_TIME = 20

TOPIC_A = "test_switch_a"
TOPIC_B = "test_switch_b"

KFK_SERVER = "kafka:9092"

g_curr_topic = TOPIC_A


c = KafkaConsumer(bootstrap_servers=KFK_SERVER, group_id="hello", enable_auto_commit=False)
c.subscribe(TOPIC_A)
topic_changed = True
g_switch_time = time.time()
buffer = []

while True:
    curr_time = time.time()
    if curr_time - g_switch_time > WAIT_TIME:
        topic = TOPIC_B if g_curr_topic == TOPIC_A else TOPIC_A
        g_curr_topic = topic
        print("switching to %s" % topic)
        c.unsubscribe()
        c.subscribe([topic])
        g_switch_time = curr_time
    if topic_changed:
        if buffer:
            assignment = c.assignment()
            if assignment:
                c.pause(*list(assignment))
        topic_changed = False
    if not buffer:
        assignment = c.assignment()
        if assignment:
            c.resume(*list(assignment))

    msgs = c.poll(timeout_ms=100, max_records=10)
    if msgs:
        if buffer:
            print("ERR: buffer not empty")
        buffer = []
        for tp, logs in msgs.items():
            logs.reverse()
            buffer.extend([(tp, log) for log in logs])
    if buffer:
        print(buffer.pop())
