from ..client_blob import get_blob_instance
BLOB_INSTANCE = get_blob_instance()

class UploadFileBlob:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "local_path": ("STRING", {"default": "input/example.png"}),
                "blob_path": ("STRING", {"default": "output/example.png"}),
            }
        }

    CATEGORY = "ComfyUI-Azure-Blob-Storage"
    INPUT_NODE = True
    OUTPUT_NODE = True
    RETURN_TYPES = ()
    FUNCTION = "upload_file_blob"

    def upload_file_blob(self, local_path, blob_path):
        BLOB_INSTANCE.upload_file(local_path, blob_path)
        print(f"Uploaded file to Blob Storage at {blob_path}")
        return {}