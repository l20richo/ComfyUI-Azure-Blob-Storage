from ..client_blob import get_blob_instance
BLOB_INSTANCE = get_blob_instance()


class DownloadFileBlob:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "blob_path": ("STRING", {"default": "input/example.png"}),
                "local_path": ("STRING", {"default": "input/example.png"}),
            }
        }
    
    CATEGORY = "ComfyUI-Azure-Blob-Storage"
    INPUT_NODE = True
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("local_path",)
    FUNCTION = "download_file_blob"
    
    def download_file_blob(self, blob_path, local_path):
        local_path = BLOB_INSTANCE.download_file(blob_path=blob_path, local_path=local_path)
        print(f"Downloaded file from Blob Storage to {local_path}")
        return local_path