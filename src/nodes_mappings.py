from .nodes.load_image_blob import LoadImageBlob
from .nodes.save_image_blob import SaveImageBlob
from .nodes.save_video_files_blob import SaveVideoFilesBlob
from .nodes.download_file_blob import DownloadFileBlob
from .nodes.upload_file_blob import UploadFileBlob


NODE_CLASS_MAPPINGS = {
    "LoadImageBLOB": LoadImageBlob,
    "SaveImageBLOB": SaveImageBlob,
    "SaveVideoFilesBLOB": SaveVideoFilesBlob,
    "DownloadFileBLOB": DownloadFileBlob,
    "UploadFileBLOB": UploadFileBlob
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageBLOB": "Load Image from ",
    "SaveImageBLOB": "Save Image to BLOB",
    "SaveVideoFilesBLOB": "Save Video Files to BLOB",
    "DownloadFileBLOB": "Download File from BLOB",
    "UploadFileBLOB": "Upload File to BLOB"
}