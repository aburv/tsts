import unittest
from unittest import mock
from unittest.mock import call

from src.config import Config
from src.option.data import FormType
from src.option.service import OptionService
from src.player.service import PlayerServices
from src.player_gear.service import PlayerGearServices
from src.player_position.service import PlayerPositionServices
from src.responses import ValidResponse, APIException, DataValidationException, CachedResponse, RecordNotFoundException, \
    RuntimeException
from src.services.auth_service import AuthServices
from src.user.service import UserServices

from test.test_app_config import get_app


class PlayerControllerTest(unittest.TestCase):

    @mock.patch.object(ValidResponse, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(ValidResponse, 'get_data', return_value='player_data')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(OptionService, '__init__', return_value=None)
    @mock.patch.object(OptionService, 'get_options', return_value='player_data')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_valid_player_options_data_response_on_get_option_data(self,
                                                                                 mock_cache_set,
                                                                                 mock_cache_get,
                                                                                 mock_token,
                                                                                 mock_api_keys,
                                                                                 mock_validate_token,
                                                                                 mock_auth_services,
                                                                                 mock_get_options,
                                                                                 mock_service_init,
                                                                                 mock_response_init,
                                                                                 mock_get_response_data,
                                                                                 mock_response
                                                                                 ):
        mock_cache_get.return_value = None
        mock_api_keys.return_value = ['test_key']
        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/player/form_data",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                }
            )

        mock_cache_get.assert_called_once_with('myapp:form_player/user_id:user_id')
        mock_cache_set.assert_called_once_with('myapp:form_player/user_id:user_id', 'player_data', timeout=60)
        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_service_init.assert_called_once_with(FormType.PLAYER)
        mock_get_options.assert_called_once_with()
        mock_response_init.assert_called_once_with('Retrieved option data', 'player_data')
        mock_get_response_data.assert_called_once_with()
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(ValidResponse, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, 'get_user_data', return_value='player_data')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value='player_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_valid_player_data_response_on_get_actual_1(self,
                                                                      mock_token,
                                                                      mock_api_keys,
                                                                      mock_validate_token,
                                                                      mock_auth_services,
                                                                      mock_get_player_id,
                                                                      mock_user_service,
                                                                      mock_get_user_data,
                                                                      mock_service_init,
                                                                      mock_response_init,
                                                                      mock_response
                                                                      ):
        mock_api_keys.return_value = ['test_key']
        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/player/actual/1",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                }
            )

        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_service_init.assert_called_once_with()
        mock_get_player_id.assert_called_once_with('user_id')
        mock_user_service.assert_called_once_with()
        mock_get_user_data.assert_called_once_with('player_id', 'user_id')
        mock_response_init.assert_called_once_with('Retrieved player user data', 'player_data')
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(APIException, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(PlayerServices, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, 'get_user_data', return_value='player_data')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value='player_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_APIException_response_on_get_actual_1(self,
                                                                 mock_token,
                                                                 mock_api_keys,
                                                                 mock_validate_token,
                                                                 mock_auth_services,
                                                                 mock_get_player_id,
                                                                 mock_user_service,
                                                                 mock_get_user_data,
                                                                 mock_service_init,
                                                                 mock_response
                                                                 ):
        mock_api_keys.return_value = ['test_key']
        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_get_user_data.side_effect = APIException(
                "message",
                "content",
                "type",
                500
            )

        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/player/actual/1",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                }
            )

        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_service_init.assert_called_once_with()
        mock_get_player_id.assert_called_once_with('user_id')
        mock_user_service.assert_called_once_with()
        mock_get_user_data.assert_called_once_with('player_id', 'user_id')
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(ValidResponse, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, 'get_by_id', return_value='player_data')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value='player_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_valid_player_data_response_on_get_actual_2(self,
                                                                      mock_token,
                                                                      mock_api_keys,
                                                                      mock_validate_token,
                                                                      mock_auth_services,
                                                                      mock_get_player_id,
                                                                      mock_user_service,
                                                                      mock_get_by_id,
                                                                      mock_service_init,
                                                                      mock_response_init,
                                                                      mock_response
                                                                      ):
        mock_api_keys.return_value = ['test_key']
        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/player/actual/2",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                }
            )

        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_service_init.assert_called_once_with()
        mock_get_player_id.assert_called_once_with('user_id')
        mock_user_service.assert_called_once_with()
        mock_get_by_id.assert_called_once_with('player_id')
        mock_response_init.assert_called_once_with('Retrieved player user data', 'player_data')
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(APIException, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(PlayerGearServices, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, 'get_by_id', return_value='player_data')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value='player_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_APIException_response_on_get_actual_2(self,
                                                                 mock_token,
                                                                 mock_api_keys,
                                                                 mock_validate_token,
                                                                 mock_auth_services,
                                                                 mock_get_player_id,
                                                                 mock_user_service,
                                                                 mock_get_by_id,
                                                                 mock_service_init,
                                                                 mock_response
                                                                 ):
        mock_api_keys.return_value = ['test_key']
        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_get_by_id.side_effect = APIException(
                "message",
                "content",
                "type",
                500
            )

        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/player/actual/2",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                }
            )

        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_service_init.assert_called_once_with()
        mock_get_player_id.assert_called_once_with('user_id')
        mock_user_service.assert_called_once_with()
        mock_get_by_id.assert_called_once_with('player_id')
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(ValidResponse, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, 'update', return_value='player_data')
    @mock.patch.object(PlayerGearServices, 'create', return_value='player_data')
    @mock.patch.object(PlayerGearServices, 'check_presence', return_value=False)
    @mock.patch.object(PlayerPositionServices, 'create_position')
    @mock.patch.object(PlayerPositionServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value='player_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_create_player_jersey_data_response_on_get_jersey_details(self,
                                                                             mock_token,
                                                                             mock_api_keys,
                                                                             mock_validate_token,
                                                                             mock_auth_services,
                                                                             mock_get_player_id,
                                                                             mock_user_service,
                                                                             mock_position_service,
                                                                             mock_create_position,
                                                                             mock_check_presence,
                                                                             mock_create,
                                                                             mock_update,
                                                                             mock_service_init,
                                                                             mock_response_init,
                                                                             mock_response
                                                                             ):
        mock_api_keys.return_value = ['test_key']
        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/player/jersey_details",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                },
                json={'data': {"positions": ["position1", "position2"]}}
            )

        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_user_service.assert_called_once_with()
        mock_get_player_id.assert_called_once_with('user_id')
        mock_service_init.assert_called_once_with()
        mock_check_presence.assert_called_once_with('player_id')
        mock_create.assert_called_once_with('player_id', {'positions': ['position1', 'position2']}, 'user_id')
        assert not mock_update.called
        mock_position_service.assert_called_once_with()
        mock_create_position.assert_has_calls([
            call('player_id', 'position1', 'user_id'),
            call('player_id', 'position2', 'user_id')
        ])
        mock_response_init.assert_called_once_with('Created player with basic details data', True)
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(APIException, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(RuntimeException, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, 'update', return_value='player_data')
    @mock.patch.object(PlayerGearServices, 'create', return_value='player_data')
    @mock.patch.object(PlayerGearServices, 'check_presence', return_value=False)
    @mock.patch.object(PlayerPositionServices, 'create_position', side_effect=Exception)
    @mock.patch.object(PlayerPositionServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value='player_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_runtime_exception_response_on_get_jersey_details(self,
                                                                     mock_token,
                                                                     mock_api_keys,
                                                                     mock_validate_token,
                                                                     mock_auth_services,
                                                                     mock_get_player_id,
                                                                     mock_user_service,
                                                                     mock_position_service,
                                                                     mock_create_position,
                                                                     mock_check_presence,
                                                                     mock_create,
                                                                     mock_update,
                                                                     mock_service_init,
                                                                     mock_exception,
                                                                     mock_response
                                                                     ):
        mock_api_keys.return_value = ['test_key']
        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/player/jersey_details",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                },
                json={'data': {"positions": ["position1", "position2"]}}
            )

        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_user_service.assert_called_once_with()
        mock_get_player_id.assert_called_once_with('user_id')
        mock_service_init.assert_called_once_with()
        mock_check_presence.assert_called_once_with('player_id')
        mock_create.assert_called_once_with('player_id', {'positions': ['position1', 'position2']}, 'user_id')
        assert not mock_update.called
        mock_position_service.assert_called_once_with()
        mock_create_position.assert_has_calls([
            call('player_id', 'position1', 'user_id'),
        ])
        mock_exception.assert_called_once_with('Unable to create positions',
                                               "{'positions': ['position1', 'position2']} on player_id ")
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(ValidResponse, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, 'update', return_value='player_data')
    @mock.patch.object(PlayerGearServices, 'create', return_value='player_data')
    @mock.patch.object(PlayerGearServices, 'check_presence', return_value=True)
    @mock.patch.object(PlayerPositionServices, 'create_position')
    @mock.patch.object(PlayerPositionServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value='player_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_update_player_jersey_data_response_on_get_jersey_details(self,
                                                                             mock_token,
                                                                             mock_api_keys,
                                                                             mock_validate_token,
                                                                             mock_auth_services,
                                                                             mock_get_player_id,
                                                                             mock_user_service,
                                                                             mock_position_service,
                                                                             mock_create_position,
                                                                             mock_check_presence,
                                                                             mock_create,
                                                                             mock_update,
                                                                             mock_service_init,
                                                                             mock_response_init,
                                                                             mock_response
                                                                             ):
        mock_api_keys.return_value = ['test_key']
        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/player/jersey_details",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                },
                json={'data': {"positions": []}}
            )

        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_user_service.assert_called_once_with()
        mock_get_player_id.assert_called_once_with('user_id')
        mock_service_init.assert_called_once_with()
        mock_check_presence.assert_called_once_with('player_id')
        assert not mock_create.called
        mock_update.assert_called_once_with('player_id', {'positions': []}, 'user_id')
        assert not mock_position_service.called
        assert not mock_create_position.called
        mock_response_init.assert_called_once_with('Updated player with basic details data', True)
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(APIException, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, 'update')
    @mock.patch.object(PlayerGearServices, 'create')
    @mock.patch.object(PlayerGearServices, 'check_presence')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value='player_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_data_validation_response_on_get_jersey_details(self,
                                                                          mock_token,
                                                                          mock_api_keys,
                                                                          mock_validate_token,
                                                                          mock_auth_services,
                                                                          mock_get_player_id,
                                                                          mock_user_service,
                                                                          mock_check_presence,
                                                                          mock_create,
                                                                          mock_update,
                                                                          mock_service_init,
                                                                          mock_exception,
                                                                          mock_response
                                                                          ):
        mock_api_keys.return_value = ['test_key']

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/player/jersey_details",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                },
                json={}
            )

        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        assert not mock_service_init.called
        assert not mock_get_player_id.called
        assert not mock_user_service.called
        assert not mock_check_presence.called
        assert not mock_create.called
        assert not mock_update.called
        mock_exception.assert_called_once_with('Create player measurements None', 'No data')
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(APIException, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(RecordNotFoundException, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, 'update')
    @mock.patch.object(PlayerGearServices, 'create')
    @mock.patch.object(PlayerGearServices, 'check_presence')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value=None)
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_record_not_found_response_on_get_jersey_details(self,
                                                                           mock_token,
                                                                           mock_api_keys,
                                                                           mock_validate_token,
                                                                           mock_auth_services,
                                                                           mock_get_player_id,
                                                                           mock_user_service,
                                                                           mock_check_presence,
                                                                           mock_create,
                                                                           mock_update,
                                                                           mock_service_init,
                                                                           mock_exception,
                                                                           mock_response
                                                                           ):
        mock_api_keys.return_value = ['test_key']

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/player/jersey_details",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                },
                json={"data": {}}
            )

        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_user_service.assert_called_once_with()
        mock_get_player_id.assert_called_once_with('user_id')
        assert not mock_service_init.called
        assert not mock_check_presence.called
        assert not mock_create.called
        assert not mock_update.called
        mock_exception.assert_called_once_with('Player for user', 'user_id')
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(APIException, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(PlayerGearServices, '__init__', return_value=None)
    @mock.patch.object(PlayerGearServices, 'update')
    @mock.patch.object(PlayerGearServices, 'create')
    @mock.patch.object(PlayerGearServices, 'check_presence')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value='player_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_APIException_response_on_get_jersey_details(self,
                                                                       mock_token,
                                                                       mock_api_keys,
                                                                       mock_validate_token,
                                                                       mock_auth_services,
                                                                       mock_get_player_id,
                                                                       mock_user_service,
                                                                       mock_check_presence,
                                                                       mock_create,
                                                                       mock_update,
                                                                       mock_service_init,
                                                                       mock_response
                                                                       ):
        mock_api_keys.return_value = ['test_key']
        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_check_presence.side_effect = APIException(
                "message",
                "content",
                "type",
                500
            )

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/player/jersey_details",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                },
                json={'data': {}}
            )

        mock_token.assert_called_once_with('token')
        mock_api_keys.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_service_init.assert_called_once_with()
        mock_get_player_id.assert_called_once_with('user_id')
        mock_user_service.assert_called_once_with()
        mock_check_presence.assert_called_once_with('player_id')
        assert not mock_create.called
        assert not mock_update.called
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(ValidResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value=None)
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, 'create', return_value='player_id')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_valid_player_id_response_on_create_player(self,
                                                                     mock_token,
                                                                     mock_secret_config,
                                                                     mock_validate_token,
                                                                     mock_auth_services,
                                                                     mock_create,
                                                                     mock_player_service,
                                                                     mock_user_service,
                                                                     mock_get_player_id,
                                                                     mock_response_init,
                                                                     mock_response
                                                                     ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/player/",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                },
                json={'data': {}}
            )

        mock_token.assert_called_once_with('token')
        mock_secret_config.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_user_service.assert_called_once_with()
        mock_get_player_id.assert_called_once_with("user_id")
        mock_player_service.assert_called_once_with()
        mock_create.assert_called_once_with({}, 'user_id')
        mock_response_init.assert_called_once_with('Created player with basic details data', 'player_id')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ValidResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(UserServices, 'get_player_id', return_value='player_id')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, 'update', return_value=None)
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_update_player_on_create_player(self,
                                                   mock_token,
                                                   mock_secret_config,
                                                   mock_validate_token,
                                                   mock_auth_services,
                                                   mock_update,
                                                   mock_player_service,
                                                   mock_user_service,
                                                   mock_get_player_id,
                                                   mock_response_init,
                                                   mock_response
                                                   ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/player/",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                },
                json={'data': {}}
            )

        mock_token.assert_called_once_with("token")
        mock_secret_config.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_user_service.assert_called_once_with()
        mock_get_player_id.assert_called_once_with("user_id")
        mock_player_service.assert_called_once_with()
        mock_update.assert_called_once_with('player_id', {}, 'user_id')
        mock_response_init.assert_called_once_with('Updated player with details data', True)
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, 'create')
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_raise_data_validation_response_when_no_data_on_create_player(self,
                                                                                 mock_token,
                                                                                 mock_secret_config,
                                                                                 mock_validate_token,
                                                                                 mock_auth_services,
                                                                                 mock_create,
                                                                                 mock_service_init,
                                                                                 mock_exception,
                                                                                 mock_response
                                                                                 ):
        mock_secret_config.return_value = ['test_key']
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/player/",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                },
                json={}
            )

        mock_token.assert_called_once_with('token')
        mock_secret_config.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        assert not mock_service_init.called
        assert not mock_create.called
        mock_exception.assert_called_once_with('Create or update player User None', 'No data')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(UserServices, 'get_player_id')
    @mock.patch.object(UserServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, '__init__', return_value=None)
    @mock.patch.object(AuthServices, 'validate_token', return_value="user_id")
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch.object(Config, 'get_tokens', return_value=("id_token", "access_token"))
    def test_should_return_api_error_response_on_create_player(self,
                                                               mock_token,
                                                               mock_secret_config,
                                                               mock_validate_token,
                                                               mock_auth_services,
                                                               mock_service_init,
                                                               mock_get_player_id,
                                                               mock_response
                                                               ):
        mock_secret_config.return_value = ['test_key']
        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_get_player_id.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.post(
                "/api/player/",
                headers={
                    'x-api-key': 'test_key',
                    'x-access-key': "token"
                },
                json={'data': {}}
            )

        mock_token.assert_called_once_with("token")
        mock_secret_config.assert_called_once_with()
        mock_validate_token.assert_called_once_with('id_token', 'access_token', '', '', '')
        mock_auth_services.assert_called_once_with()
        mock_service_init.assert_called_once_with()
        mock_get_player_id.assert_called_once_with('user_id')
        mock_response.assert_called_once_with()
        self.assertEqual(expected_response_data, actual_response.data)

    @mock.patch.object(ValidResponse, 'get_response_json', return_value={'data': 'player_data'})
    @mock.patch.object(ValidResponse, 'get_data', return_value='player_data')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, 'get_player_info', return_value='player_data')
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_valid_player_data_response_on_get_player(self,
                                                                    mock_cache_set,
                                                                    mock_cache_get,
                                                                    mock_api_keys,
                                                                    mock_get_player_info,
                                                                    mock_service_init,
                                                                    mock_response_init,
                                                                    mock_get_response_data,
                                                                    mock_response
                                                                    ):
        mock_cache_get.return_value = None
        mock_api_keys.return_value = ['test_key']
        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/player/player_id",
                headers={
                    'x-api-key': 'test_key',
                }
            )

        mock_cache_get.assert_called_once_with('myapp:player_info/r_id:player_id')
        mock_cache_set.assert_called_once_with('myapp:player_info/r_id:player_id', 'player_data', timeout=60)
        mock_service_init.assert_called_once_with()
        mock_get_player_info.assert_called_once_with('player_id')
        mock_response_init.assert_called_once_with('Retrieved player data', 'player_data')
        mock_get_response_data.assert_called_once_with()
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'{"data":"player_data"}\n')

    @mock.patch.object(CachedResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(CachedResponse, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, 'get_player_info', return_value='player_data')
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_cached_player_data_response_on_get_player(self,
                                                                     mock_cache_set,
                                                                     mock_cache_get,
                                                                     mock_api_keys,
                                                                     mock_get_player_info,
                                                                     mock_service_init,
                                                                     mock_response_init,
                                                                     mock_response,
                                                                     ):
        mock_cache_get.return_value = {'data': 'player_data'}
        mock_api_keys.return_value = ['test_key']
        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/player/player_id",
                headers={
                    'x-api-key': 'test_key',
                }
            )

        mock_cache_get.assert_called_once_with('myapp:player_info/r_id:player_id')
        assert not mock_cache_set.called
        assert not mock_service_init.called
        assert not mock_get_player_info.called
        mock_response_init.assert_called_once_with(key='myapp:player_info/r_id:player_id', data={'data': 'player_data'})
        mock_response.assert_called_once_with()

        self.assertEqual(actual_response.data, b'response_json')

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(PlayerServices, '__init__', return_value=None)
    @mock.patch.object(PlayerServices, 'get_player_info', return_value='player_data')
    @mock.patch.object(Config, 'get_api_keys')
    @mock.patch('flask_caching.Cache.get')
    @mock.patch('flask_caching.Cache.set')
    def test_should_return_api_error_response_on_get_player(self,
                                                            mock_cache_set,
                                                            mock_cache_get,
                                                            mock_secret_config,
                                                            mock_get_player_info,
                                                            mock_service_init,
                                                            mock_response
                                                            ):
        mock_cache_get.return_value = None
        mock_secret_config.return_value = ['test_key']

        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_get_player_info.side_effect = APIException(
                "msg",
                "content",
                "error_type",
                500
            )
        expected_response_data = b'response_json'

        app = get_app()
        with app.test_client() as c:
            actual_response = c.get(
                "/api/player/player_id",
                headers={
                    'x-api-key': 'test_key',
                }
            )

        mock_cache_get.assert_called_once_with('myapp:player_info/r_id:player_id')
        assert not mock_cache_set.called
        mock_service_init.assert_called_once_with()
        mock_get_player_info.assert_called_once_with('player_id')
        mock_response.assert_called_once_with()

        self.assertEqual(expected_response_data, actual_response.data)
