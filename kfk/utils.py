from kafka.protocol.admin import (
    CreateTopicsRequest_v1,
    CreateTopicsResponse_v1,
    DeleteTopicsRequest_v0,
    DeleteTopicsResponse_v0,
    ListGroupsRequest_v0,
    ListGroupsResponse_v0,
    DescribeGroupsRequest_v0,
    DescribeGroupsResponse_v0,
)


def create_topics(cli, timeout, topics):
    create_topic_requests = [
        [topic, 1, 1, [], []] if isinstance(topic, str)
        else [
            topic['name'],
            topic.get('partitions', 1),
            topic.get('replication_factor', 1),
            [],
            topic.get('configs', []),
        ]
        for topic in topics
    ]
    msg = [
        create_topic_requests,
        timeout,
        False,
    ]
    create_topic_msg = CreateTopicsRequest_v1(*msg)
    nodeId = list(cli.cluster.brokers())[0].nodeId
    cli.send(nodeId, create_topic_msg)
    res = cli.poll(timeout_ms=timeout)
    return res[0]


def delete_topics(cli, timeout, topics):
    msg = [
        topics,
        timeout,
    ]
    delete_topic_msg = DeleteTopicsRequest_v0(*msg)
    nodeId = list(cli.cluster.brokers())[0].nodeId
    cli.send(nodeId, delete_topic_msg)
    res = cli.poll(timeout_ms=timeout)
    return res[0]


def list_groups(cli, timeout):
    nodeId = list(cli.cluster.brokers())[0].nodeId
    cli.send(nodeId, ListGroupsRequest_v0())
    res = cli.poll(timeout_ms=timeout)
    return res[0]


def describe_groups(cli, timeout, groups):
    describe_groups_msg = DescribeGroupsRequest_v0(groups)
    nodeId = list(cli.cluster.brokers())[0].nodeId
    cli.send(nodeId, ListGroupsRequest_v0())
    res = cli.poll(timeout_ms=timeout)
    return res[0]
