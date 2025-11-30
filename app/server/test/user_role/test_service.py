import unittest
from unittest import mock

from src.db_duo import PostgresDbDuo
from src.user_role.data import UserRoleData
from src.user_role.service import UserRoleServices


class UserRoleServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserRoleData, '__init__', return_value=None)
    def test_should_init_user_role_service(self,
                                           mock_data,
                                           mock_db):
        actual = UserRoleServices()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], UserRoleData)
        self.assertIsInstance(actual, UserRoleServices)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, 'insert_record', return_value=True)
    @mock.patch.object(UserRoleData, '__init__', return_value=None)
    def test_should_insert_user_role_on_assign_user_permission(self,
                                                               mock_data,
                                                               mock_insert,
                                                               mock_db):
        mock_data.get.side_effect = ["user_id_id"]
        with mock.patch.object(UserRoleServices, '__init__', return_value=None):
            service = UserRoleServices()
            service._data = mock_data
            service._db = mock_db
            mock_db.insert_record = mock_insert

        service.assign_user_permission({}, "u_id")

        mock_data.on_data.assert_called_once_with({})
        mock_insert.assert_called_once()
        mock_insert.assert_called_once_with("u_id", r_id="u_id")

    @mock.patch.object(PostgresDbDuo, 'get_records')
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserRoleData, '__init__', return_value=None)
    def test_should_return_user_id_data_on_get_user_permission(self,
                                                               mock_data,
                                                               mock_db,
                                                               mock_get_records):
        mock_get_records.return_value = [{"data": "user_role_data"}]

        with mock.patch.object(UserRoleServices, '__init__', return_value=None):
            service = UserRoleServices()
            service._db = mock_db
            service._data = mock_data
            mock_db.get_records = mock_get_records

        actual = service.get_user_permission("user_id")

        mock_get_records.assert_called_once_with()
        mock_data.on_data.assert_called_once_with({'user': 'user_id'})

        self.assertEqual(actual, [{"data": "user_role_data"}])
