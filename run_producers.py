import time
import threading

from kafka import KafkaProducer

TOPIC_A = "test_switch_a"
TOPIC_B = "test_switch_b"

KFK_SERVER = "kafka:9092"


class Producer(threading.Thread):
    def __init__(self, topic):
        super(Producer, self).__init__(name=topic)
        self.topic = topic
        self._msg_counter = 0
        self.producer = KafkaProducer(bootstrap_servers=KFK_SERVER)

    def get_msg(self):
        self._msg_counter += 1
        return "%s-%d" % (self.topic, self._msg_counter)

    def run(self):
        while True:
            msg = self.get_msg()
            self.producer.send(self.topic, value=msg)
            print(msg)
            time.sleep(0.1)


def main():
    pa = Producer(TOPIC_A)
    pb = Producer(TOPIC_B)
    pa.start()
    pb.start()
    pa.join()
    pb.join()

if __name__ == "__main__":
    main()
