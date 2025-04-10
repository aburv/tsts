import unittest
from unittest import mock
from unittest.mock import call

from src.config import Relation
from src.data import DataModel
from src.login.data import UserLoginData


class LoginDataTest(unittest.TestCase):

    @mock.patch.object(DataModel, '__init__', return_value=None)
    def test_should_init_login_data(self, mock_model):
        data = UserLoginData()

        mock_model.assert_called_once_with(Relation.LOGIN, has_id=False, is_a_record=False)
        self.assertIsInstance(data, UserLoginData)

    @mock.patch.object(DataModel, 'set_data')
    def test_should_call_set_login_data_on_data(self, mock_set):
        with mock.patch.object(UserLoginData, '__init__', return_value=None):
            data = UserLoginData()

        data.on_data({})

        mock_set.assert_called_once_with({}, True)

    @mock.patch.object(DataModel, 'add_field')
    def test_should_add_login_fields_on_add_insert_fields(self, mock_add_field):
        with mock.patch.object(UserLoginData, '__init__', return_value=None):
            UserLoginData().add_insert_fields()

        mock_add_field.assert_has_calls([
            call('t_user', 'userId', str, is_optional=False),
            call('device', 'deviceId', str, is_optional=False),
            call('l_location', 'locationId', str),
            call('ipv4', 'ip', str, is_optional=False)
        ])

    def test_should_return_none_on_add_fields(self):
        with mock.patch.object(UserLoginData, '__init__', return_value=None):
            data = UserLoginData()

        actual = data.add_fields()

        self.assertIsNone(actual)
