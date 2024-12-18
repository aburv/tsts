import unittest
from unittest import mock

from src.db_duo import PostgresDbDuo
from src.image.data import ImageData
from src.image.service import ImageServices


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
