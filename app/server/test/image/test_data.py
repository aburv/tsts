import unittest
from unittest import mock
from unittest.mock import call, MagicMock

from src.config import Relation
from src.data import DataModel
from src.image.data import ImageData


class ImageDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_image_data(self, mock_model):
        data = ImageData()

        mock_model.assert_called_once_with(Relation.IMAGE, is_a_record=False)
        self.assertIsInstance(data, ImageData)

    @mock.patch('werkzeug.datastructures.FileStorage')
    @mock.patch.object(DataModel, 'set_data')
    @mock.patch.object(ImageData, 'resize_and_compress')
    @mock.patch('PIL.Image.open', new_callable=MagicMock)
    def test_should_call_set_image_data_on_data(self,
                                                mock_image_open,
                                                mock_resize_and_compress,
                                                mock_set,
                                                mock_file):
        mock_resize_and_compress.side_effect = [b"compressed", b"one", b"two", b"three"]
        img_file = mock_file.return_value
        img_file.filename = "name"
        img_file.read.return_value = b"file_data_bytes"

        mock_img = MagicMock()
        mock_image_open.return_value = mock_img

        data = {
            "name": "name",
            "c_data": b'compressed',
            "data": b"file_data_bytes",
            "one": b"one",
            "two": b"two",
            "three": b"three"
        }

        with mock.patch.object(ImageData, '__init__', return_value=None):
            img_data = ImageData()
            img_data._has_id = True
            img_data._is_a_record = False
            img_data._fields = {}

        img_data.on_data(img_file)

        mock_image_open.assert_called_once_with(img_file.stream)
        mock_img.load.assert_called_once_with()
        mock_resize_and_compress.assert_has_calls([
            call(mock_img, None),
            call(mock_img, (80, 80)),
            call(mock_img, (160, 160)),
            call(mock_img, (320, 320))
        ])
        mock_set.assert_called_once_with(data, True)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_set_data_to_select_on_select(self, mock_set):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            image_data = ImageData()

        image_data.on_select({}, "")

        mock_set.assert_called_once_with({}, False)
        self.assertEqual(image_data._filter_type, "")

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_image_fields_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(ImageData, '__init__', return_value=None):
            ImageData().add_insert_fields()

        mock_add_field.assert_has_calls([
            call('i_name', 'name', str),
            call('original', 'data', bytes, is_optional=False),
            call('c_original', 'c_data', bytes, is_optional=False),
            call('one', 'one', bytes, is_optional=False),
            call('two', 'two', bytes, is_optional=False),
            call('three', 'three', bytes, is_optional=False)
        ])

    @mock.patch.object(DataModel, 'add_field', return_value=None)
    def test_should_return_none_on_add_fields(self, mock_add_field):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            image_data = ImageData()

        image_data.add_fields()

        mock_add_field.assert_has_calls([
            call('id', 'id', str)
        ])

    def test_should_return_empty_dict_on_get_audit_fields(self):
        with mock.patch.object(ImageData, '__init__', return_value=None):
            data = ImageData()
            actual = data.get_audit_payload()

        self.assertEqual({}, actual)

    @mock.patch('PIL.Image.open', new_callable=MagicMock)
    @mock.patch('zlib.compress', return_value=b'image_compressed_resized_bytes')
    @mock.patch('io.BytesIO', return_value=None)
    def test_should_return_resized_compress_bytes_on_resize_and_compress(self,
                                                                         mock_bytesio,
                                                                         mock_compress,
                                                                         mock_open):
        mock_bytes_io = MagicMock()
        mock_bytesio.return_value = mock_bytes_io
        mock_bytes_io.getvalue.return_value = b'image_resized_bytes'

        mock_resized = MagicMock()
        mock_open.resize.return_value = mock_resized

        actual = ImageData.resize_and_compress(mock_open, (80, 80))

        mock_open.resize.assert_called_once_with((80, 80))
        mock_bytesio.assert_called_once_with()
        mock_resized.save.assert_called_once_with(mock_bytes_io, format="PNG")
        mock_bytes_io.getvalue.assert_called_once_with()
        mock_compress.assert_called_once_with(b'image_resized_bytes')
        self.assertEqual(b'image_compressed_resized_bytes', actual)

    @mock.patch('PIL.Image.open', new_callable=MagicMock)
    @mock.patch('zlib.compress', return_value=b'image_compressed_resized_bytes')
    @mock.patch('io.BytesIO')
    def test_should_return_compressed_bytes_on_resize_and_compress(self,
                                                                   mock_bytesio,
                                                                   mock_compress,
                                                                   mock_open):
        mock_bytes_io = MagicMock()
        mock_bytesio.return_value = mock_bytes_io
        mock_bytes_io.getvalue.return_value = b'image_resized_bytes'

        actual = ImageData.resize_and_compress(mock_open, None)

        assert not mock_open.resize.called
        mock_bytesio.assert_called_once_with()
        mock_open.save.assert_called_once_with(mock_bytes_io, format="PNG")
        mock_bytes_io.getvalue.assert_called_once_with()
        mock_compress.assert_called_once_with(b'image_resized_bytes')
        self.assertEqual(b'image_compressed_resized_bytes', actual)

    def test_should_return_one_on_get_record_count(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            image_data = ImageData()

        actual = image_data.get_record_count()

        self.assertEqual(1, actual)

    def test_should_return_query_fields_on_get_querying_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            image_data = ImageData()

        actual = image_data.get_querying_fields()

        self.assertEqual(['id'], actual)

    def test_should_return_one_on_get_filtering_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            image_data = ImageData()
            image_data._filter_type = "80"

        actual = image_data.get_filtering_fields()

        self.assertEqual(['one'], actual)

    def test_should_return_two_on_get_filtering_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            image_data = ImageData()
            image_data._filter_type = "160"

        actual = image_data.get_filtering_fields()

        self.assertEqual(['two'], actual)

    def test_should_return_three_on_get_filtering_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            image_data = ImageData()
            image_data._filter_type = "320"

        actual = image_data.get_filtering_fields()

        self.assertEqual(['three'], actual)

    def test_should_return_c_original_on_get_filtering_fields(self):
        with mock.patch.object(DataModel, '__init__', return_value=None):
            image_data = ImageData()
            image_data._filter_type = None

        actual = image_data.get_filtering_fields()

        self.assertEqual(['c_original'], actual)
