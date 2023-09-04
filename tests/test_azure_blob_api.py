import time
import unittest
from caixa_de_ferramentas.azure_blob_api import BlobClientApi, BlobAdminApi
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


class TestBlobAdminApi(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        credential = DefaultAzureCredential()
        storage_account = 'dadaiastorage'
        cls.blob_client = BlobAdminApi(storage_account, credential=credential)
        cls.container_name = 'container-test'
        cls.blob_client.create_container(cls.container_name)

  
    def test_list_blobs(self):
        blob_list = self.blob_client.list_blobs(self.container_name)
        print(blob_list)
        self.assertEqual(len(blob_list), 0)


    def test_upload_delete_blob(self):
        file_src = 'tests/inbound/testblob.txt'
        file_dst = 'testblob.txt'
        self.blob_client.upload_blob(self.container_name, file_src, file_dst)
        blob_list = self.blob_client.list_blobs(self.container_name)
        self.assertEqual(len(blob_list), 1)
        self.assertEqual(blob_list[0], file_dst)
        self.blob_client.delete_blob(self.container_name, file_dst)


    def test_download_blob(self):
        file_src = 'tests/inbound/testblob.txt'
        file_dst = 'testblob.txt'
        path_download = 'tests/outbound/testblob.txt'
        self.blob_client.upload_blob(self.container_name, file_src, file_dst)
        self.blob_client.download_blob(self.container_name, file_dst, path_download)
        self.blob_client.delete_blob(self.container_name, file_dst)
        with open(path_download, 'r') as f:
            self.assertEqual(f.read(), 'testando 1, 2, 3...')


if __name__ == "__main__":
    unittest.main(TestBlobAdminApi())