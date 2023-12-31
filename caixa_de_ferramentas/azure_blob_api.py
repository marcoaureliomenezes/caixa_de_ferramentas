from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import tracemalloc

tracemalloc.start()

class BlobClientApi:

    def __init__(self, storage_account, credential):
        account_url=f"https://{storage_account}.blob.core.windows.net/"
        self.blob_service_client = BlobServiceClient(account_url, credential=credential)


    def upload_blob(self, container_name, file_src, file_dst):  
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_dst)
        try: 
            with open(file_src, "rb") as data:
                blob_client.upload_blob(data)
        except ResourceExistsError: print(f'Blob {file_dst} already exists')
        return blob_client
    

    def download_blob(self, container_name, file_src, file_dst):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_src)
        with open(file_dst, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        return blob_client
    

    def delete_blob(self, container_name, blob_name):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.delete_blob()
        return blob_client
    
    
    def list_blobs(self, container_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs()
        list_blobs = [i['name'] for i in blob_list]
        return list_blobs
    

    def list_containers(self):
        container_list = self.blob_service_client.list_containers()
        list_container = [i['name'] for i in container_list]
        return list_container
    

class BlobAdminApi(BlobClientApi):

    def __init__(self, storage_account, credential):
        super().__init__(storage_account, credential)


    def create_container(self, container_name):
        try: container_client = self.blob_service_client.create_container(container_name)
        except ResourceExistsError: 
            print(f'Container {container_name} already exists')
            container_client = self.blob_service_client.get_container_client(container_name)
        return container_client


    def delete_container(self, container_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        container_client.delete_container()
        return container_client
    


if __name__ == '__main__':
    pass