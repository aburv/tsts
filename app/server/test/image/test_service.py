import unittest
from io import BytesIO
from unittest import mock
from unittest.mock import MagicMock

from werkzeug.datastructures import FileStorage

from src.db_duo import PostgresDbDuo
from src.image.data import ImageData
from src.image.service import ImageServices
from src.responses import RuntimeException


class ImageServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(ImageData, '__init__', return_value=None)
    def test_should__init_image_service(self,
                                        mock_data,
                                        mock_db):
        actual = ImageServices()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], ImageData)
        self.assertIsInstance(actual, ImageServices)

    @mock.patch('werkzeug.datastructures.FileStorage')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(ImageData, '__init__', return_value=None)
    def test_should_return_inserted_image_id_on_add(self,
                                                    mock_image_data,
                                                    mock_insert,
                                                    mock_db,
                                                    mock_file):
        mock_image_data.get.side_effect = ["image_id"]
        with mock.patch.object(ImageServices, '__init__', return_value=None):
            service = ImageServices()
            service._data = mock_image_data
            service._db = mock_db
            mock_db.insert_record = mock_insert

        actual = service.add(mock_file, "")

        mock_image_data.on_data.assert_called_once_with(mock_file)
        mock_image_data.get.assert_called_once_with('id')
        mock_insert.assert_called_once()
        mock_insert.assert_called_once_with("")

        self.assertEqual(actual, "image_id")

    @mock.patch.object(ImageServices, 'add', return_value="image_id")
    @mock.patch('src.image.service.FileStorage')
    @mock.patch('src.image.service.BytesIO')
    @mock.patch('requests.get')
    def test_should_return_inserted_image_id_after_load_on_load_and_save(self,
                                                                         mock_request_get,
                                                                         mock_io_byteio,
                                                                         mock_file,
                                                                         mock_image_add
                                                                         ):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'image_byte'
        mock_request_get.return_value = mock_response

        mock_bytes_io_instance = MagicMock(spec=BytesIO)
        mock_io_byteio.return_value = mock_bytes_io_instance

        mock_file_storage_instance = MagicMock(spec=FileStorage)
        mock_file.return_value = mock_file_storage_instance

        with mock.patch.object(ImageServices, '__init__', return_value=None):
            service = ImageServices()

        actual = service.load_and_save("url", "u_id")

        mock_io_byteio.assert_called_once_with(mock_response.content)
        mock_file.assert_called_once_with(mock_bytes_io_instance, "u_id")

        mock_image_add.assert_called_once_with(mock_file(), "u_id")

        self.assertEqual(actual, "image_id")

    @mock.patch.object(RuntimeException, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'add', return_value="image_id")
    @mock.patch('src.image.service.FileStorage')
    @mock.patch('src.image.service.BytesIO')
    @mock.patch('requests.get')
    def test_should_raise_runtime_exception_when_load_is_not_success_on_load_and_save(self,
                                                                                      mock_request_get,
                                                                                      mock_io_byteio,
                                                                                      mock_file,
                                                                                      mock_image_add,
                                                                                      mock_exception
                                                                                      ):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.content = b'image_byte'
        mock_request_get.return_value = mock_response

        mock_bytes_io_instance = MagicMock(spec=BytesIO)
        mock_io_byteio.return_value = mock_bytes_io_instance

        mock_file_storage_instance = MagicMock(spec=FileStorage)
        mock_file.return_value = mock_file_storage_instance

        with mock.patch.object(ImageServices, '__init__', return_value=None):
            service = ImageServices()

        with self.assertRaises(RuntimeException):
            service.load_and_save("url", "u_id")

        assert not mock_io_byteio.called
        assert not mock_file.called

        assert not mock_image_add.called

        mock_exception.assert_called_once_with("Unable to load an image", "url u_id")

    @mock.patch('zlib.decompress', return_value=b'image_bytes')
    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(ImageData, '__init__', return_value=None)
    def test_should_return_c_original_image_str_on_get(self,
                                                       mock_data,
                                                       mock_db,
                                                       mock_get_records,
                                                       mock_decompress):
        mock_data.get_filtering_fields.return_value = ['c_original']
        mock_get_records.return_value = [{"c_original": b"image_compressed_bytes"}]

        with mock.patch.object(ImageServices, '__init__', return_value=None):
            service = ImageServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        actual = service.get("img_id", None)

        mock_get_records.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'id': 'img_id'}, None)

        mock_data.get_filtering_fields.assert_called_once_with()
        mock_decompress.assert_called_once_with(b"image_compressed_bytes")
        self.assertEqual(actual, b"image_bytes")

    @mock.patch('zlib.decompress', return_value=b'image_bytes')
    @mock.patch.object(PostgresDbDuo, 'get_records', return_value=[])
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(ImageData, '__init__', return_value=None)
    def test_should_return_empty_image_str_when_no_data_from_db_on_get(self,
                                                                       mock_data,
                                                                       mock_db,
                                                                       mock_get_records,
                                                                       mock_decompress):
        with mock.patch.object(ImageServices, '__init__', return_value=None):
            service = ImageServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        actual = service.get("img_id", "")

        mock_get_records.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'id': 'img_id'}, "")

        assert not mock_data.get_filtering_fields.called
        assert not mock_decompress.called
        self.assertEqual(actual, b"")
