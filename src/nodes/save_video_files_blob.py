import os

from ..client_blob import get_blob_instance
BLOB_INSTANCE = get_blob_instance()


class SaveVideoFilesBlob:
    def __init__(self):
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "filename_prefix": ("STRING", {"default": "VideoFiles"}),
            "filenames": ("VHS_FILENAMES", )
            }}

    RETURN_TYPES = ()
    FUNCTION = "save_video_files"
    OUTPUT_NODE = True
    CATEGORY = "ComfyUI-Azure-Blob-Storage"

    def save_video_files(self, filenames, filename_prefix="VideoFiles"):
        filename_prefix += self.prefix_append
        local_files = filenames[1]
        full_output_folder, filename, counter, _, filename_prefix = BLOB_INSTANCE.get_save_path(filename_prefix)
        
        for path in local_files:
            ext = path.split(".")[-1]
            file = f"{filename}_{counter:05}_.{ext}"
            
            # Upload the local file to S3
            blob_path = os.path.join(full_output_folder, file)
            BLOB_INSTANCE.upload_file(path, blob_path)
        
        return {}
    
