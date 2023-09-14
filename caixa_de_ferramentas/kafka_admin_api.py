import json, asyncio
from abc import ABC, abstractmethod
from kafka import KafkaProducer, KafkaConsumer
import os, sys, time
from kafka.admin import NewTopic, KafkaAdminClient, ConfigResource, ConfigResourceType
from kafka.errors import TopicAlreadyExistsError


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    


class KafkaAdminAPI(metaclass=SingletonMeta):

    def __init__(self, connection_str):
        self.connection_str = connection_str
        self.admin = KafkaAdminClient(bootstrap_servers=self.connection_str)


    def create_idempotent_topic(self, topic, num_partitions=1, replication_factor=1, overwrite=False, topic_config=None):
        topic_blocks = NewTopic(name=topic, num_partitions=num_partitions, replication_factor=replication_factor, topic_configs=topic_config)

        try: self.admin.create_topics(new_topics=[topic_blocks], validate_only=False)
        except TopicAlreadyExistsError: 
            if overwrite:
                self.admin.delete_topics([topic])
                time.sleep(5)
                self.admin.create_topics(new_topics=[topic_blocks], validate_only=False)
                return "TOPIC DELETED AND CREATED AGAIN"
            return "TOPIC ALREADY CREATED AND KEPT"
        else: return "TOPIC CREATED"


    def update_topic(self, topic, configs):
        cfg_resource_update = ConfigResource(ConfigResourceType.TOPIC, topic,configs=configs)
        self.admin.alter_configs([cfg_resource_update])


    def delete_topic(self, topic):
        admin = KafkaAdminClient(bootstrap_servers=self.connection_str)
        admin.delete_topics([topic])
        return "TOPIC DELETED"


    def list_topics(self):
        return self.admin.list_topics()


    def describe_topic(self, topic):
        return self.admin.describe_topics([topic])
    
    
    # See the retention time of a topic

    def get_topic_config(self, topic):
        cfg_resource = ConfigResource(ConfigResourceType.TOPIC, topic)
        return self.admin.describe_configs([cfg_resource])




if __name__ == '__main__':
    
    kafka_broker = "localhost:9092"
    topic = "test"
    kafka_admin = KafkaAdminAPI(kafka_broker)
    print(kafka_admin.list_topics())