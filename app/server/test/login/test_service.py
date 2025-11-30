import unittest
from unittest import mock
from unittest.mock import call

from src.config import Config
from src.db_duo import PostgresDbDuo
from src.image.service import ImageServices
from src.location.service import LocationServices
from src.login.data import UserLoginData
from src.login.service import LoginServices
from src.responses import DataValidationException, RecordNotFoundException
from src.services.auth_service import AuthServices
from src.user.service import UserServices
from src.user_id.service import UserIdServices
from src.user_role.service import UserRoleServices


class LoginServiceTest(unittest.TestCase):

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserLoginData, '__init__', return_value=None)
    def test_should_init_login_service(self,
                                       mock_data,
                                       mock_db
                                       ):
        actual = LoginServices()

        mock_data.assert_called_once_with()
        mock_db.assert_called_once()
        args, _ = mock_db.call_args
        self.assertIsInstance(args[0], UserLoginData)
        self.assertIsInstance(actual, LoginServices)

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserRoleServices, '__init__', return_value=None)
    @mock.patch.object(UserRoleServices, 'assign_user_permission', return_value=None)
    @mock.patch.object(UserLoginData, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, 'get_user_id_by_id_value', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'create_user', return_value="user_id")
    @mock.patch.object(UserServices, 'update_user', return_value=None)
    @mock.patch.object(LocationServices, 'get_location_id_by_long_lat', return_value=None)
    @mock.patch.object(LocationServices, 'create_location', return_value="location_id")
    @mock.patch.object(LocationServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'load_and_save', return_value="i_id")
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'login', return_value=("id_token", "access_token"))
    def test_should_create_new_user_and_login_with_new_location_and_pic_url_on_login(self,
                                                                                     mock_login,
                                                                                     mock_auth_service,
                                                                                     mock_image_service,
                                                                                     mock_load_and_save,
                                                                                     mock_location_service,
                                                                                     mock_create_location,
                                                                                     mock_get_location,
                                                                                     mock_update_user,
                                                                                     mock_create_user,
                                                                                     mock_user_service,
                                                                                     mock_get_user_id_by_id,
                                                                                     mock_user_id_service,
                                                                                     mock_data,
                                                                                     mock_assign_role,
                                                                                     mock_role_service,
                                                                                     mock_db):
        user_data = {
            "uId": {
                "value": "id"
            },
            "idToken": "id_token",
            "picUrl": "url"
        }
        login_data = {
            "location": {'lat': 'lat', 'long': 'long'}
        }
        with mock.patch.object(LoginServices, '__init__', return_value=None):
            service = LoginServices()
            service._data = mock_data
            service._db = mock_db

        actual = service.login(user_data, login_data)

        mock_user_id_service.assert_called_once_with()
        mock_get_user_id_by_id.assert_called_once_with('id')
        mock_user_service.assert_has_calls([call(), call()])
        mock_create_user.assert_called_once_with({'uId': {'value': 'id'}, 'idToken': 'id_token', 'picUrl': 'url'})
        mock_location_service.assert_has_calls([call(), call()])
        mock_get_location.assert_called_once_with("long", "lat")
        mock_create_location.assert_called_once_with({'lat': 'lat', 'long': 'long'}, 'user_id')
        mock_image_service.assert_called_once_with()
        mock_load_and_save.assert_called_once_with('url', 'user_id')
        mock_update_user.assert_called_once_with({'id': 'user_id', 'dp': 'i_id'}, 'user_id')
        mock_data.on_data.assert_called_once_with(
            {'location': {'lat': 'lat', 'long': 'long'}, 'userId': 'user_id', 'locationId': 'location_id'})
        mock_db.insert_record.assert_called_once_with("user_id", "user_id")
        mock_assign_role.assert_called_once_with({'user': 'user_id', 'resource': 'I', 'record_id': 'i_id', 'permission': 'V'}, 'user_id')
        mock_role_service.assert_called_once_with()
        mock_auth_service.assert_called_once_with()
        mock_login.assert_called_once_with("user_id")

        self.assertEqual(actual, {'accessToken': 'access_token', 'idToken': 'id_token'})

    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserLoginData, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, 'get_user_id_by_id_value', return_value="user_id")
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_by_id', return_value={"user": "data"})
    @mock.patch.object(UserServices, 'create_user', return_value=None)
    @mock.patch.object(UserServices, 'update_user', return_value=None)
    @mock.patch.object(LocationServices, 'create_location')
    @mock.patch.object(LocationServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'load_and_save', return_value="i_id")
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'login', return_value=("id_token", "access_token"))
    def test_should_create_login_with_existing_user_without_location_on_login(self,
                                                                              mock_login,
                                                                              mock_auth_service,
                                                                              mock_image_services,
                                                                              mock_load_and_save,
                                                                              mock_location_services,
                                                                              mock_create_location,
                                                                              mock_update_user,
                                                                              mock_create_user,
                                                                              mock_get_user_by_id,
                                                                              mock_user_service,
                                                                              mock_get_user_id_by_id,
                                                                              mock_user_id_service,
                                                                              mock_data,
                                                                              mock_db):
        user_data = {
            "uId": {
                "value": "id"
            },
            "idToken": "id_token"
        }
        login_data = {
            "location": None
        }
        with mock.patch.object(LoginServices, '__init__', return_value=None):
            service = LoginServices()
            service._data = mock_data
            service._db = mock_db

        actual = service.login(user_data, login_data)

        mock_user_id_service.assert_called_once_with()
        mock_get_user_id_by_id.assert_called_once_with('id')
        mock_user_service.assert_called_once_with()
        assert not mock_create_user.called
        assert not mock_create_location.called
        assert not mock_location_services.called
        assert not mock_update_user.called
        assert not mock_image_services.called
        assert not mock_load_and_save.called
        mock_get_user_by_id.assert_called_once_with('user_id')
        mock_data.on_data.assert_called_once_with({"location": None, 'userId': 'user_id'})
        mock_db.insert_record.assert_called_once_with('user_id', 'user_id')
        mock_auth_service.assert_called_once_with()
        mock_login.assert_called_once_with("user_id")

        self.assertEqual(actual, {'accessToken': 'access_token', 'idToken': 'id_token'})

    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserLoginData, '__init__', return_value=None)
    @mock.patch.object(UserRoleServices, '__init__', return_value=None)
    @mock.patch.object(UserRoleServices, 'assign_user_permission', return_value=None)
    @mock.patch.object(UserIdServices, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, 'get_user_id_by_id_value', return_value=None)
    @mock.patch.object(UserIdServices, 'get_user_ids_by_user', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value=None)
    @mock.patch.object(UserServices, 'create_user', return_value="user_id")
    @mock.patch.object(UserServices, 'update_user', return_value=None)
    @mock.patch.object(LocationServices, 'get_location_id_by_long_lat', return_value=None)
    @mock.patch.object(LocationServices, 'create_location', return_value="location_id")
    @mock.patch.object(LocationServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'load_and_save', return_value="i_id")
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'login', return_value=("id_token", "access_token"))
    def test_should_raise_datavalidation_exception_when_no_location_data_on_login(self,
                                                                                  mock_login,
                                                                                  mock_auth_service,
                                                                                  mock_image_service,
                                                                                  mock_load_and_save,
                                                                                  mock_location_service,
                                                                                  mock_create_location,
                                                                                  mock_get_location,
                                                                                  mock_update_user,
                                                                                  mock_create_user,
                                                                                  mock_get_user_data,
                                                                                  mock_user_service,
                                                                                  mock_user_ids_by_user,
                                                                                  mock_get_user_id_by_id,
                                                                                  mock_user_id_service,
                                                                                  mock_assign_role,
                                                                                  mock_role_service,
                                                                                  mock_data,
                                                                                  mock_db,
                                                                                  mock_exception):
        user_data = {
            "uId": {
                "value": "id"
            },
            "idToken": "id_token",
            "picUrl": "url"
        }
        login_data = {
            "location": {"long": ""}
        }
        with mock.patch.object(LoginServices, '__init__', return_value=None):
            service = LoginServices()
            service._data = mock_data
            service._db = mock_db

        with self.assertRaises(DataValidationException):
            service.login(user_data, login_data)

        mock_user_id_service.assert_called_once_with()
        mock_get_user_id_by_id.assert_called_once_with('id')
        mock_user_service.assert_has_calls([call(), call()])
        mock_create_user.assert_called_once_with({'uId': {'value': 'id'}, 'idToken': 'id_token', 'picUrl': 'url'})
        assert not mock_get_user_data.called
        assert not mock_user_ids_by_user.called
        assert not mock_location_service.called
        assert not mock_get_location.called
        assert not mock_create_location.called
        mock_image_service.assert_called_once_with()
        mock_load_and_save.assert_called_once_with('url', 'user_id')
        mock_update_user.assert_called_once_with({'id': 'user_id', 'dp': 'i_id'}, 'user_id')
        assert not mock_data.on_data.called
        assert not mock_db.insert_record.called
        assert not mock_auth_service.called
        assert not mock_login.called
        mock_assign_role.assert_called_once_with({'user': 'user_id', 'resource': 'I', 'record_id': 'i_id', 'permission': 'V'}, 'user_id')
        mock_role_service.assert_called_once_with()

        mock_exception.assert_called_once_with('Get Location', "Necessary fields not present: 'lat'")

    @mock.patch.object(RecordNotFoundException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserLoginData, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, 'get_user_id_by_id_value', return_value="user_id")
    @mock.patch.object(UserIdServices, 'get_user_ids_by_user', return_value=[{"value": "mail_id", "type": "m"}])
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_by_id', return_value=None)
    @mock.patch.object(UserServices, 'create_user', return_value=None)
    @mock.patch.object(UserServices, 'update_user', return_value=None)
    @mock.patch.object(LocationServices, 'create_location')
    @mock.patch.object(LocationServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'load_and_save', return_value="i_id")
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'login', return_value=("id_token", "access_token"))
    def test_should_raise_record_not_found_with_existing_user_id_on_login(self,
                                                                          mock_login,
                                                                          mock_auth_service,
                                                                          mock_image_services,
                                                                          mock_load_and_save,
                                                                          mock_location_services,
                                                                          mock_create_location,
                                                                          mock_update_user,
                                                                          mock_create_user,
                                                                          mock_get_user_by_id,
                                                                          mock_user_service,
                                                                          mock_user_ids_by_user,
                                                                          mock_get_user_id_by_id,
                                                                          mock_user_id_service,
                                                                          mock_data,
                                                                          mock_db,
                                                                          mock_exception):
        user_data = {
            "uId": {
                "value": "id"
            },
            "idToken": "id_token"
        }
        login_data = {}
        with mock.patch.object(LoginServices, '__init__', return_value=None):
            service = LoginServices()
            service._data = mock_data
            service._db = mock_db

        with self.assertRaises(RecordNotFoundException):
            service.login(user_data, login_data)

        mock_user_id_service.assert_called_once_with()
        mock_get_user_id_by_id.assert_called_once_with('id')
        mock_user_service.assert_called_once_with()
        assert not mock_create_user.called
        assert not mock_create_location.called
        assert not mock_location_services.called
        assert not mock_update_user.called
        assert not mock_image_services.called
        assert not mock_load_and_save.called
        mock_get_user_by_id.assert_called_once_with("user_id")
        assert not mock_user_ids_by_user.called
        assert not mock_data.on_data.called
        assert not mock_db.insert_record.called
        assert not mock_auth_service.called
        assert not mock_login.called

        mock_exception.assert_called_once_with('User', 'user_id')

    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserLoginData, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, 'get_user_id_by_id_value', return_value="user_id")
    @mock.patch.object(UserIdServices, 'get_user_ids_by_user', return_value=[{"value": "mail_id", "type": "m"}])
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value={})
    @mock.patch.object(UserServices, 'create_user', return_value=None)
    @mock.patch.object(UserServices, 'update_user', return_value=None)
    @mock.patch.object(LocationServices, 'create_location')
    @mock.patch.object(LocationServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'load_and_save', return_value="i_id")
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'login', return_value=("id_token", "access_token"))
    def test_should_raise_data_validation_exception_when_no_uid_key_on_login(self,
                                                                             mock_login,
                                                                             mock_image_services,
                                                                             mock_load_and_save,
                                                                             mock_location_services,
                                                                             mock_create_location,
                                                                             mock_update_user,
                                                                             mock_create_user,
                                                                             mock_get_user_data,
                                                                             mock_user_service,
                                                                             mock_user_ids_by_user,
                                                                             mock_get_user_id_by_id,
                                                                             mock_user_id_service,
                                                                             mock_data,
                                                                             mock_db,
                                                                             mock_exception):
        user_data = {}
        login_data = {}
        with mock.patch.object(LoginServices, '__init__', return_value=None):
            service = LoginServices()
            service._data = mock_data
            service._db = mock_db

        with self.assertRaises(DataValidationException):
            service.login(user_data, login_data)

        mock_exception.assert_called_once_with("Login", 'No Id data')
        assert not mock_user_id_service.called
        assert not mock_get_user_id_by_id.called
        assert not mock_user_service.called
        assert not mock_create_user.called
        assert not mock_create_location.called
        assert not mock_location_services.called
        assert not mock_update_user.called
        assert not mock_image_services.called
        assert not mock_load_and_save.called
        assert not mock_get_user_data.called
        assert not mock_user_ids_by_user.called
        assert not mock_data.on_data.called
        assert not mock_db.insert_record.called
        assert not mock_login.called

    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(PostgresDbDuo, '__init__', return_value=None)
    @mock.patch.object(UserLoginData, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, '__init__', return_value=None)
    @mock.patch.object(UserIdServices, 'get_user_id_by_id_value', return_value="user_id")
    @mock.patch.object(UserIdServices, 'get_user_ids_by_user', return_value=[{"value": "mail_id", "type": "m"}])
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_user_data', return_value={})
    @mock.patch.object(UserServices, 'create_user', return_value=None)
    @mock.patch.object(UserServices, 'update_user', return_value=None)
    @mock.patch.object(LocationServices, 'create_location')
    @mock.patch.object(LocationServices, '__init__', return_value=None)
    @mock.patch.object(ImageServices, 'load_and_save', return_value="i_id")
    @mock.patch.object(ImageServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'login', return_value=("id_token", "access_token"))
    def test_should_raise_data_validation_exception_when_no_uid_value_key_on_login(self,
                                                                                   mock_login,
                                                                                   mock_image_services,
                                                                                   mock_load_and_save,
                                                                                   mock_location_services,
                                                                                   mock_create_location,
                                                                                   mock_update_user,
                                                                                   mock_create_user,
                                                                                   mock_get_user_data,
                                                                                   mock_user_service,
                                                                                   mock_user_ids_by_user,
                                                                                   mock_get_user_id_by_id,
                                                                                   mock_user_id_service,
                                                                                   mock_data,
                                                                                   mock_db,
                                                                                   mock_exception):
        user_data = {
            "uId": {
                "type": ""
            }
        }
        login_data = {}
        with mock.patch.object(LoginServices, '__init__', return_value=None):
            service = LoginServices()
            service._data = mock_data
            service._db = mock_db

        with self.assertRaises(DataValidationException):
            service.login(user_data, login_data)

        mock_exception.assert_called_once_with("Login", 'No Id value')
        assert not mock_user_id_service.called
        assert not mock_get_user_id_by_id.called
        assert not mock_user_service.called
        assert not mock_create_user.called
        assert not mock_create_location.called
        assert not mock_location_services.called
        assert not mock_update_user.called
        assert not mock_image_services.called
        assert not mock_load_and_save.called
        assert not mock_get_user_data.called
        assert not mock_user_ids_by_user.called
        assert not mock_data.on_data.called
        assert not mock_db.insert_record.called
        assert not mock_login.called

    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'refresh_token', return_value=("new_id_token", "new_access_token"))
    @mock.patch.object(Config, 'get_tokens', return_value=("exp_id_token", "exp_access_token"))
    def test_should_return_tokens_on_refresh(self,
                                             mock_get_tokens,
                                             mock_refresh_token,
                                             mock_auth_services):
        actual = LoginServices.refresh("token")

        mock_get_tokens.assert_called_once_with('token')
        mock_refresh_token.assert_called_once_with('exp_id_token', 'exp_access_token')
        mock_auth_services.assert_called_once_with()

        self.assertEqual({'accessToken': 'new_access_token', 'idToken': 'new_id_token'}, actual)

    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'refresh_token')
    @mock.patch.object(Config, 'get_tokens')
    def test_should_return_empty_obj_when_datavalidation_exception_raised_on_refresh(self,
                                                                                     mock_get_tokens,
                                                                                     mock_refresh_token,
                                                                                     mock_auth_services):
        with mock.patch.object(DataValidationException, "__init__", return_value=None):
            mock_get_tokens.side_effect = DataValidationException("msg", "content")

        actual = LoginServices.refresh("token")

        mock_get_tokens.assert_called_once_with('token')
        assert not mock_refresh_token.called
        assert not mock_auth_services.called

        self.assertEqual({}, actual)
