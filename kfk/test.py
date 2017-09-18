import time
import kafka
import logging

from kafka.client_async import KafkaClient
from kafka.protocol.admin import CreateTopicsRequest_v1

from . utils import (
    create_topics,
    delete_topics,
    list_groups,
    describe_groups,
)

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)

client_configs = {
    "bootstrap_servers": ["kafka:9092"],
    "client_id": "kafka_test_admin",
#    "api_version": KafkaClient.API_VERSIONS[0],
}

client = KafkaClient(**client_configs)

# print(create_topics(client, 1000, ["hello", "world"]))

res = list_groups(client, 1000)
print res