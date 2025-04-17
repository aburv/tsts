"""
Image Service
"""
import zlib
from io import BytesIO

import requests
from werkzeug.datastructures import FileStorage

from src.db_duo import PostgresDbDuo
from src.image.data import ImageData
from src.responses import RuntimeException


class ImageServices:
    """
    Service on Image
    """

    def __init__(self):
        self._data = ImageData()
        self._db = PostgresDbDuo(self._data)

    def add(self, file: FileStorage, user_id: str) -> str:
        """
        :return:
        :rtype:
        """
        image_data = file
        self._data.on_data(image_data)
        self._db.insert_record(user_id)
        return self._data.get("id")

    def load_and_save(self, pic_url: str, u_id: str) -> str:
        """
        Load and save image and return id
        """
        response = requests.get(pic_url, timeout=600)
        if response.status_code != 200:
            raise RuntimeException("Unable to load an image", f"{pic_url} {u_id}")
        data = BytesIO(response.content)
        file = FileStorage(data, u_id)
        return self.add(file, u_id)

    def get(self, i_id: str, size: str | None) -> bytes:
        """
        Get image by id
        """
        self._data.on_select({"id": i_id}, size)
        data = self._db.get_records()
        if len(data) > 0:
            return zlib.decompress(data[0][self._data.get_filtering_fields()[0]])
        return b''
