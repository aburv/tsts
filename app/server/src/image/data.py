"""
Image Data
"""
import io
import zlib

from PIL import Image
from werkzeug.datastructures.file_storage import FileStorage

from src.config import Relation
from src.data import DataModel


class ImageData(DataModel):
    """
    Data Image
    """

    def __init__(self):
        super().__init__(Relation.IMAGE, is_a_record=False)

    def on_data(self, image_file: FileStorage):
        """
        Set up Image data
        """
        image_byte = image_file.read()
        img = Image.open(image_file.stream)
        img.load()

        data = {
            "name": image_file.filename,
            "data": image_byte,
            "c_data": self.resize_and_compress(img, None),
            "one": self.resize_and_compress(img, (80, 80)),
            "two": self.resize_and_compress(img, (160, 160)),
            "three": self.resize_and_compress(img, (320, 320))
        }
        self.set_data(data, True)

    def on_select(self, data: dict, _filter_type: str):
        """
        sets on select data
        """
        self.set_data(data, False)
        self._filter_type = _filter_type

    def add_insert_fields(self):
        self.add_field('i_name', "name", str)
        self.add_field('original', "data", bytes, is_optional=False)
        self.add_field('c_original', "c_data", bytes, is_optional=False)
        self.add_field('one', "one", bytes, is_optional=False)
        self.add_field('two', "two", bytes, is_optional=False)
        self.add_field('three', "three", bytes, is_optional=False)

    def add_fields(self):
        self.add_field('id', "id", str)

    def get_audit_payload(self) -> dict:
        return {}

    def get_filtering_fields(self) -> list:
        f_field = "c_original"
        if self._filter_type == "80":
            f_field = "one"
        elif self._filter_type == "160":
            f_field = "two"
        elif self._filter_type == "320":
            f_field = "three"
        return [f_field]

    def get_querying_fields(self) -> list:
        return ['id']

    def get_record_count(self) -> int | None:
        return 1

    @staticmethod
    def resize_and_compress(image: Image, size: tuple | None) -> bytes:
        """
        Resize and compress image
        """
        if size is not None:
            img_resized = image.resize(size)
        else:
            img_resized = image

        buffered = io.BytesIO()
        img_resized.save(buffered, format='PNG')
        img_bytes = buffered.getvalue()

        compressed_image = zlib.compress(img_bytes)
        return compressed_image
