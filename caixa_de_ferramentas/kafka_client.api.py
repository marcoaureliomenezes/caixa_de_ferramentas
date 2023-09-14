import json
from kafka import KafkaConsumer, KafkaProducer


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
    

class KafkaClient(metaclass=SingletonMeta):

  
    def __init__(self, connection_str):
        self.connection_str = connection_str


    def create_producer(self):
        partitioner = lambda key, all, available: 0
        json_serializer = lambda data: json.dumps(data).encode('utf-8')
        producer = KafkaProducer(
                                        bootstrap_servers=self.connection_str,
                                        value_serializer=json_serializer, 
                                        partitioner=partitioner
        )
        return producer
   

    def create_consumer(self, topic, consumer_group):
        consumer = KafkaConsumer(
                                        topic, 
                                        bootstrap_servers=self.connection_str, 
                                        auto_offset_reset='latest', 
                                        group_id=consumer_group
        )
        return consumer


    def send_data(self, producer, topic, data, partition=None, key="0"):
        producer.send(topic=topic, key=f"topic_{key}".encode('utf-8'), partition=partition, value=data)
        producer.flush()   