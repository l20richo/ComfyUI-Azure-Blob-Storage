import os
from .logger import logger
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
load_dotenv()

class Blob:
    def __init__(self, storage_account_name, connection_string, container_name):
        
        self.storage_account_name = storage_account_name
        self.connection_string = connection_string
        self.container_name = container_name
        self.blob_service_client = self.get_client()

        self.input_dir = os.getenv("BLOB_INPUT_DIR")
        self.output_dir = os.getenv("BLOB_OUTPUT_DIR")
        if not self.does_folder_exist(self.input_dir):
            self.create_folder(self.output_dir)
        if not self.does_folder_exist(self.output_dir):
            self.create_folder(self.output_dir)

    def get_client(self):
        if not all([self.storage_account_name, self.connection_string, self.container_name]):
            err = "Missing required Azure environment variables."
            logger.error(err)
    
        try:
           
            blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            return blob_service_client
        except Exception as e:
            err = f"Failed to create Blob client: {e}"
            logger.error(err)

    def get_files(self, prefix):
        if self.does_folder_exist(prefix):
            try:
                container_client = self.blob_service_client.get_container_client(self.container_name)
                blobs = container_client.list_blobs(name_starts_with=prefix)
                files = [blob.name.replace(prefix, "") for blob in blobs]
                return files
            except Exception as e:
                err = f"Failed to get files from Blob Storage: {e}"
                logger.error(err)
        else:
            return []
    
    def does_folder_exist(self, folder_name):
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            response =  container_client.list_blobs(name_starts_with=folder_name+"/")
            for obj in response:
                return True
            return False
        except Exception as e:
            err = f"Failed to check if folder exists in Blob: {e}"
            logger.error(err)
    
    def create_folder(self, folder_name):
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(f"{folder_name}/")
            blob_client.upload_blob(b"", overwrite=True)

        except Exception as e:
            err = f"Failed to create folder in Blob: {e}"
            logger.error(err)
    
    def download_file(self, blob_path, local_path):
        local_dir = os.path.dirname(local_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        try:
            
            blob_client = self.blob_service_client.get_blob_client(container= self.container_name, blob = blob_path)

            with open(local_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            return local_path
        except ResourceNotFoundError:
            err = "Credentials not available or not valid."
            logger.error(err)
        except Exception as e:
            err = f"Failed to download file from Blob Storage: {e}"
            logger.error(err)

    def upload_file(self, local_path, blob_path):
        try:
            blob_client = self.blob_service_client.get_blob_client(container= self.container_name, blob = blob_path)
            with open(local_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)

            return blob_path
        except ResourceNotFoundError:
            err = "Credentials not available or not valid."
            logger.error(err)
        except Exception as e:
            err = f"Failed to upload file to Blob Storage: {e}"
            logger.error(err)
    
    def get_save_path(self, filename_prefix, image_width=0, image_height=0):
        def map_filename(filename):
            prefix_len = len(os.path.basename(filename_prefix))
            prefix = filename[:prefix_len + 1]
            try:
                digits = int(filename[prefix_len + 1:].split('_')[0])
            except:
                digits = 0
            return (digits, prefix)

        def compute_vars(input, image_width, image_height):
            input = input.replace("%width%", str(image_width))
            input = input.replace("%height%", str(image_height))
            return input

        filename_prefix = compute_vars(filename_prefix, image_width, image_height)
        subfolder = os.path.dirname(os.path.normpath(filename_prefix))
        filename = os.path.basename(os.path.normpath(filename_prefix))
        
        full_output_folder_blob = os.path.join(self.output_dir, subfolder)
        
        # Check if the output folder exists, create it if it doesn't
        if not self.does_folder_exist(full_output_folder_blob):
            self.create_folder(full_output_folder_blob)

        try:
            # Continue with the counter calculation
            files = self.get_files(full_output_folder_blob)
            counter = max(
                filter(
                    lambda a: a[1][:-1] == filename and a[1][-1] == "_",
                    map(map_filename, files)
                )
            )[0] + 1
        except (ValueError, KeyError):
            counter = 1
        
        return full_output_folder_blob, filename, counter, subfolder, filename_prefix


def get_blob_instance():
    try:
        blob_instance = Blob(
            storage_account_name=os.getenv("AZURE_STORAGE_ACCOUNT_NAME"),
            connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
            container_name=os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        )

        return blob_instance
    except Exception as e:
        err = f"Failed to create Azure Blob instance: {e} Please check your environment variables."
        logger.error(err)