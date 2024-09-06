from base64 import b64decode
import os
import uuid

appdir = os.path.abspath(os.path.dirname(__file__))
absolutePath = os.path.dirname(appdir)
storagePath = "../../uploads/assets"


class AssetService:
    def __init__(self):
        pass

    def upload_file(self, base64: str, filename: str):
        filename, file_extension = os.path.splitext(filename)
        unique_filename = uuid.uuid4().hex + file_extension
        subpath = "media"
        media_directory = os.path.join(absolutePath, storagePath, subpath)
        if not os.path.exists(media_directory):
            os.makedirs(media_directory)
        with open(os.path.join(media_directory, unique_filename), "wb") as fh:
            fh.write(b64decode(base64.split(",")[1]))

        file_location = os.path.join(subpath, unique_filename)
        return {"url": file_location}
