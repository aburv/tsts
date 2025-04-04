import unittest
from unittest import mock

from src.db_duo import PostgresDbDuo
from src.user_id.data import UserIDData
from src.user_id.service import UserIdServices


class UserIdServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserIDData, '__init__', return_value=None)
    def test_should_init_user_id_service(self,
                                         mock_data,
                                         mock_db):
        actual = UserIdServices()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], UserIDData)
        self.assertIsInstance(actual, UserIdServices)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(UserIDData, '__init__', return_value=None)
    def test_should_insert_user_id_on_create_user_id(self,
                                                     mock_user_id_data,
                                                     mock_insert,
                                                     mock_db):
        mock_user_id_data.get.side_effect = ["user_id_id"]
        with mock.patch.object(UserIdServices, '__init__', return_value=None):
            service = UserIdServices()
            service._data = mock_user_id_data
            service._db = mock_db
            mock_db.insert_record = mock_insert

        service.create_user_id({"user": "u_id"}, "u_id")

        mock_user_id_data.on_data.assert_called_once_with({'user': 'u_id'})
        mock_insert.assert_called_once()
        mock_insert.assert_called_once_with('u_id', 'u_id')

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserIDData, '__init__', return_value=None)
    def test_should_return_user_id_data_on_get_user_id_by_id(self,
                                                             mock_data,
                                                             mock_db):
        with mock.patch.object(UserIdServices, '__init__', return_value=None):
            service = UserIdServices()
            mock_db.get_records.return_value = [{"data": "user_id_data"}]
            service._db = mock_db
            service._data = mock_data

        actual = service.get_user_ids_by_user("user_id")

        mock_db.get_records.assert_called_once_with()
        mock_data.on_select.assert_called_once_with({'user': 'user_id', 'is_verified': True})

        self.assertEqual(actual, [{"data": "user_id_data"}])

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserIDData, '__init__', return_value=None)
    def test_should_return_user_id_on_get_user_id_by_id_value(self,
                                                              mock_data,
                                                              mock_db):
        with mock.patch.object(UserIdServices, '__init__', return_value=None):
            service = UserIdServices()
            mock_db.get_records.return_value = [{"id": "user_id"}]
            mock_data.get_filtering_fields.return_value = ["id"]
            service._db = mock_db
            service._data = mock_data

        actual = service.get_user_id_by_id_value("user_mail_id")

        mock_data.on_select.assert_called_once_with({'value': 'user_mail_id', 'is_verified': True}, 'id')
        mock_db.get_records.assert_called_once_with()
        mock_data.get_filtering_fields.assert_called_once_with()

        self.assertEqual(actual, "user_id")

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserIDData, '__init__', return_value=None)
    def test_should_return_none_when_no_id_on_get_user_id_by_id_value(self,
                                                                      mock_data,
                                                                      mock_db):
        with mock.patch.object(UserIdServices, '__init__', return_value=None):
            service = UserIdServices()
            mock_db.get_records.return_value = []
            mock_data.get_filtering_fields.return_value = ["id"]
            service._db = mock_db
            service._data = mock_data

        actual = service.get_user_id_by_id_value("user_mail_id")

        mock_data.on_select.assert_called_once_with({'value': 'user_mail_id', 'is_verified': True}, 'id')
        mock_db.get_records.assert_called_once_with()
        assert not mock_data.get_filtering_fields.called

        self.assertEqual(actual, None)
