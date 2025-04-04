import unittest
from unittest import mock

from src.db_duo import PostgresDbDuo
from src.user.data import UserData
from src.user.service import UserServices
from src.user_id.service import UserIdServices


class UserServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserData, '__init__', return_value=None)
    def test_should__init_user_service(self,
                                       mock_data,
                                       mock_db
                                       ):
        actual = UserServices()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], UserData)
        self.assertIsInstance(actual, UserServices)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(UserIdServices, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, 'create_user_id', return_value=None)
    @mock.patch.object(UserData, '__init__', return_value=None)
    def test_should_create_user_and_return_user_id_on_create_user(self,
                                                                  mock_user_data,
                                                                  mock_create_user_id,
                                                                  mock_user_id_service,
                                                                  mock_insert,
                                                                  mock_db):
        mock_user_data.get.side_effect = ["user_id"]
        user_data = {
            "uId": {"val": "mail_id", "type": "mail"}
        }
        with mock.patch.object(UserServices, '__init__', return_value=None):
            service = UserServices()
            service._data = mock_user_data
            service._db = mock_db
            mock_db.insert_record = mock_insert

        actual = service.create_user(user_data)

        mock_user_data.on_data.assert_called_once_with(user_data, True)
        mock_user_id_service.assert_called_once_with()
        mock_create_user_id.assert_called_once_with(
            {
                'val': 'mail_id',
                'type': 'mail',
                'user': 'user_id',
                'isVerified': True
            },
            "user_id"
        )
        mock_user_data.get.assert_called_once_with('id')
        mock_insert.assert_called_once_with("user_id")

        self.assertEqual(actual, "user_id")

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'update_record', return_value=True)
    @mock.patch.object(UserData, '__init__', return_value=None)
    def test_should_update_user_data_on_update_user(self,
                                                    mock_user_data,
                                                    mock_update,
                                                    mock_db):
        with mock.patch.object(UserServices, '__init__', return_value=None):
            service = UserServices()
            service._data = mock_user_data
            service._db = mock_db
            mock_db.update_record = mock_update

        service.update_user({"id": "u_id"})

        mock_user_data.on_data.assert_called_once_with({'id': 'u_id'}, False)
        mock_update.assert_called_once_with('u_id')

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserData, '__init__', return_value=None)
    def test_should_return_user_data_on_get_user_by_id(self,
                                                       mock_user_data,
                                                       mock_db):
        with mock.patch.object(UserServices, '__init__', return_value=None):
            service = UserServices()
            mock_db.get_records.return_value = [{"data": "user"}]
            service._data = mock_user_data
            service._db = mock_db

        actual = service.get_user_by_id("user_id")

        mock_user_data.on_select.assert_called_once_with({'id': 'user_id', 'is_active': True}, 'id')
        mock_db.get_records.assert_called_once_with()

        self.assertEqual(actual, {"data": "user"})

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserData, '__init__', return_value=None)
    def test_should_return_empty_on_get_user_by_id(self,
                                                   mock_user_data,
                                                   mock_db):
        with mock.patch.object(UserServices, '__init__', return_value=None):
            service = UserServices()
            mock_db.get_records.return_value = []
            service._data = mock_user_data
            service._db = mock_db

        actual = service.get_user_by_id("user_id")

        mock_user_data.on_select.assert_called_once_with({'id': 'user_id', 'is_active': True}, 'id')
        mock_db.get_records.assert_called_once_with()

        self.assertEqual(actual, None)

    def test_should_return_empty_dict_on_get_user_data(self):
        with mock.patch.object(UserServices, '__init__', return_value=None):
            service = UserServices()
        expected = {}

        actual = service.get_user_data('data')

        self.assertEqual(actual, expected)
