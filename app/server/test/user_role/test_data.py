import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.data import DataModel
from src.user_role.data import UserRoleData


class UserDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_user_data(self, mock_model):
        data = UserRoleData()

        mock_model.assert_called_once_with(Relation.ROLE, has_id=False, is_a_record=False)
        self.assertIsInstance(data, UserRoleData)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_user_role_data_on_data(self, mock_set):
        with mock.patch.object(UserRoleData, '__init__', return_value=None):
            data = UserRoleData()

        data.on_data({})

        mock_set.assert_called_once_with({}, True)

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_user_role_fields_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(UserRoleData, '__init__', return_value=None):
            UserRoleData().add_insert_fields()

        mock_add_field.assert_has_calls([
            call('user', 'user', str, is_optional=False),
            call('record_id', 'id', str, is_optional=False),
            call('permission', 'permission', str, is_optional=False)
        ])

    def test_should_return_user_role_querying_fields_on_get_querying_fields(self):
        with mock.patch.object(UserRoleData, '__init__', return_value=None):
            actual = UserRoleData().get_querying_fields()

        self.assertEqual(actual, ["user"])

    def test_should_return_user_role_filtering_fields_on_get_filtering_fields(self):
        with mock.patch.object(UserRoleData, '__init__', return_value=None):
            actual = UserRoleData().get_filtering_fields()

        self.assertEqual(actual, ["record_id", "permission"])

    def test_should_return_none_on_add_fields(self):
        with mock.patch.object(UserRoleData, '__init__', return_value=None):
            data = UserRoleData()

        actual = data.add_fields()

        self.assertIsNone(actual)
