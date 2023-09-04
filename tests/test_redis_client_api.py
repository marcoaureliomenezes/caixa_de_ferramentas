import unittest
from caixa_de_ferramentas.redis_client_api import RedisAPI


class TestRedisClient(unittest.TestCase):

    redis_client = RedisAPI(host='localhost', port=36379)

    def test_clear_keys(self):
        key, value = 'test_key', 'test_value'
        self.redis_client.insert_key(key, value)
        self.redis_client.clear_keys()
        self.assertEqual(self.redis_client.list_keys(), [])


    def test_list_keys(self):
        self.redis_client.clear_keys()
        key_1, value_1 = 'test_key_1', 'test_value_1'
        key_2, value_2 = 'test_key_2', 'test_value_2'
        self.redis_client.insert_key(key_1, value_1)
        self.redis_client.insert_key(key_2, value_2)
        keys = self.redis_client.list_keys()
        self.assertEqual(len(keys), 2)
        self.assertEqual(keys[0], key_1)
        self.assertEqual(keys[1], key_2)


    def test_insert_key(self):
        self.redis_client.clear_keys()
        key, value = 'test_key', 'test_value'
        self.redis_client.insert_key(key, value)
        self.assertEqual(self.redis_client.get_key(key), value)
        self.redis_client.delete_key(key)


    def test_insert_key_with_overwrite(self):
        key_1, value_1 = 'test_key_1', 'test_value_1'
        key_1, value_2 = 'test_key_1', 'test_value_2'
        self.redis_client.insert_key(key_1, value_1)
        self.redis_client.insert_key(key_1, value_2, overwrite=True)
        self.assertEqual(self.redis_client.get_key(key_1), value_2)
        self.redis_client.clear_keys()


    def test_insert_key_without_overwrite(self):
        key_1, value_1 = 'test_key_1', 'test_value_1'
        key_1, value_2 = 'test_key_1', 'test_value_2'
        self.redis_client.insert_key(key_1, value_1)
        self.redis_client.insert_key(key_1, value_2, overwrite=False)
        self.assertEqual(self.redis_client.get_key(key_1), value_1)
        self.redis_client.clear_keys()


    def test_get_key(self):
        self.redis_client.clear_keys()
        key, value = 'test_key', 'test_value'
        self.redis_client.insert_key(key, value)
        self.assertEqual(self.redis_client.get_key(key), value)
        self.redis_client.delete_key(key)


    def test_delete_key(self):
        key, value = 'test_key', 'test_value'
        self.redis_client.insert_key(key, value)
        self.redis_client.delete_key(key)
        self.assertEqual(self.redis_client.get_key(key), [])
        self.redis_client.clear_keys()

if __name__ == "__main__":
    unittest.main(TestRedisClient())