import unittest
from unittest import mock

from src.client.service import ClientSessionService
from src.responses import APIException, DataValidationException, ValidResponse
from test.test_app_config import get_app


class ClientControllerTest(unittest.TestCase):

    @mock.patch.object(ValidResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, 'create_challenge', return_value='challenge-token')
    def test_should_return_challenge_on_create_challenge(
            self,
            mock_create_challenge,
            mock_response_init,
            mock_response
    ):
        app = get_app()

        with app.test_client() as client:
            actual_response = client.post(
                "/api/client/challenge",
                json={
                    'data': {
                        'installationId': 'installation-1234',
                        'publicKey': 'cHVibGljLWtleQ==',
                        'platform': 'ios',
                    }
                },
            )

        mock_create_challenge.assert_called_once_with(
            'installation-1234', 'cHVibGljLWtleQ==', 'ios'
        )
        mock_response_init.assert_called_once_with(
            'Client', {'challenge': 'challenge-token'}
        )
        mock_response.assert_called_once_with()
        self.assertEqual(b'response_json', actual_response.data)

    @mock.patch.object(ValidResponse, 'get_response_json', return_value='response_json')
    @mock.patch.object(ValidResponse, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, 'create_from_challenge',
                       return_value=('client-token', 1234567890))
    def test_should_return_client_token_on_create_session(
            self,
            mock_create_from_challenge,
            mock_response_init,
            mock_response
    ):
        app = get_app()

        with app.test_client() as client:
            actual_response = client.post(
                "/api/client/session",
                json={
                    'installationId': 'installation-1234',
                    'platform': 'web',
                    'challenge': 'challenge-token',
                    'signature': 'c2lnbmF0dXJl',
                },
            )

        mock_create_from_challenge.assert_called_once_with(
            'installation-1234', 'web', 'challenge-token', 'c2lnbmF0dXJl'
        )
        mock_response_init.assert_called_once_with(
            'Client', {'clientToken': 'client-token', 'expiresAt': 1234567890}
        )
        mock_response.assert_called_once_with()
        self.assertEqual(b'response_json', actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, 'create_challenge')
    def test_should_return_validation_error_for_invalid_challenge_data(
            self, mock_create_challenge, mock_exception, mock_response
    ):
        app = get_app()

        with app.test_client() as client:
            actual_response = client.post(
                "/api/client/challenge",
                json={'data': {
                    'installationId': 'short',
                    'publicKey': 'not-base64',
                    'platform': 'ios',
                }},
            )

        mock_create_challenge.assert_not_called()
        mock_exception.assert_called_once_with(
            'Installation', 'Invalid installation ID'
        )
        mock_response.assert_called_once_with()
        self.assertEqual(b'response_json', actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, 'create_challenge')
    def test_should_return_validation_error_for_invalid_challenge_platform(
            self, mock_create_challenge, mock_exception, mock_response
    ):
        app = get_app()

        with app.test_client() as client:
            actual_response = client.post(
                "/api/client/challenge",
                json={'data': {
                    'installationId': 'installation-1234',
                    'publicKey': 'cHVibGljLWtleQ==',
                    'platform': 'desktop',
                }},
            )

        mock_create_challenge.assert_not_called()
        mock_exception.assert_called_once_with('Platform', 'Invalid platform')
        mock_response.assert_called_once_with()
        self.assertEqual(b'response_json', actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, 'create_challenge')
    def test_should_return_validation_error_for_invalid_public_key(
            self, mock_create_challenge, mock_exception, mock_response
    ):
        app = get_app()

        with app.test_client() as client:
            actual_response = client.post(
                "/api/client/challenge",
                json={'data': {
                    'installationId': 'installation-1234',
                    'publicKey': 'not-base64',
                    'platform': 'ios',
                }},
            )

        mock_create_challenge.assert_not_called()
        mock_exception.assert_called_once_with('Public key', 'Invalid public key')
        mock_response.assert_called_once_with()
        self.assertEqual(b'response_json', actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, 'create_from_challenge')
    def test_should_return_validation_error_for_invalid_session_data(
            self, mock_create_from_challenge, mock_exception, mock_response
    ):
        app = get_app()

        with app.test_client() as client:
            actual_response = client.post(
                "/api/client/session",
                json={'data': {
                    'installationId': 'installation-1234',
                    'platform': 'desktop',
                    'challenge': 'challenge-token',
                    'signature': 'c2lnbmF0dXJl',
                }},
            )

        mock_create_from_challenge.assert_not_called()
        mock_exception.assert_called_once_with('Platform', 'Invalid platform')
        mock_response.assert_called_once_with()
        self.assertEqual(b'response_json', actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(DataValidationException, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, 'create_from_challenge')
    def test_should_return_validation_error_for_invalid_session_installation(
            self, mock_create_from_challenge, mock_exception, mock_response
    ):
        app = get_app()

        with app.test_client() as client:
            actual_response = client.post(
                "/api/client/session",
                json={'data': {
                    'installationId': 'short',
                    'platform': 'web',
                    'challenge': 'challenge-token',
                    'signature': 'c2lnbmF0dXJl',
                }},
            )

        mock_create_from_challenge.assert_not_called()
        mock_exception.assert_called_once_with(
            'Installation', 'Invalid installation ID'
        )
        mock_response.assert_called_once_with()
        self.assertEqual(b'response_json', actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(ClientSessionService, 'create_challenge')
    def test_should_return_api_error_on_create_challenge_failure(
            self, mock_create_challenge, mock_response
    ):
        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_create_challenge.side_effect = APIException(
                'msg', 'content', 'error_type', 500
            )
        app = get_app()

        with app.test_client() as client:
            actual_response = client.post(
                "/api/client/challenge",
                json={'data': {
                    'installationId': 'installation-1234',
                    'publicKey': 'cHVibGljLWtleQ==',
                    'platform': 'android',
                }},
            )

        mock_create_challenge.assert_called_once_with(
            'installation-1234', 'cHVibGljLWtleQ==', 'android'
        )
        mock_response.assert_called_once_with()
        self.assertEqual(b'response_json', actual_response.data)

    @mock.patch.object(APIException, 'get_response_json', return_value='response_json')
    @mock.patch.object(ClientSessionService, 'create_from_challenge')
    def test_should_return_api_error_on_create_session_failure(
            self, mock_create_from_challenge, mock_response
    ):
        with mock.patch.object(APIException, '__init__', return_value=None):
            mock_create_from_challenge.side_effect = APIException(
                'msg', 'content', 'error_type', 401
            )
        app = get_app()

        with app.test_client() as client:
            actual_response = client.post(
                "/api/client/session",
                json={'data': {
                    'installationId': 'installation-1234',
                    'platform': 'android',
                    'challenge': 'challenge-token',
                    'signature': 'c2lnbmF0dXJl',
                }},
            )

        mock_create_from_challenge.assert_called_once_with(
            'installation-1234', 'android', 'challenge-token', 'c2lnbmF0dXJl'
        )
        mock_response.assert_called_once_with()
        self.assertEqual(b'response_json', actual_response.data)
