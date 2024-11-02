"""
Image Service
"""
import zlib

from werkzeug.datastructures.file_storage import FileStorage

from src.db_duo import PostgresDbDuo
from src.image.data import ImageData


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

    def get(self, i_id: str, size: str | None) -> bytes:
        """
        Get image by id
        """
        self._data.on_select({"id": i_id}, size)
        data = self._db.get_records()
        if len(data) > 0:
            return zlib.decompress(data[0][self._data.get_filtering_fields()[0]])
        return b''
