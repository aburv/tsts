import unittest
from unittest import mock

from cryptography.exceptions import InvalidSignature

from src.caching import Caching
from src.client.service import ClientSessionService
from src.responses import SecurityException


class ClientSessionServiceTest(unittest.TestCase):

    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.json.dumps', return_value='record-json')
    @mock.patch('src.client.service.time.time', return_value=1000)
    @mock.patch('src.client.service.secrets.token_urlsafe', return_value='client-token')
    def test_should_create_client_session_and_store_records(
            self, mock_token, mock_time, mock_dumps, mock_cache, mock_hash
    ):
        actual = ClientSessionService.create('installation-id', 'public-key', 'ios')

        self.assertEqual(('client-token', 4600), actual)
        mock_token.assert_called_once_with(32)
        mock_time.assert_called_once_with()
        expected_record = {
            'installation_id': 'installation-id',
            'public_key': 'public-key',
            'platform': 'ios',
            'expires_at': 4600,
        }
        self.assertEqual(2, mock_dumps.call_count)
        mock_dumps.assert_has_calls([mock.call(expected_record), mock.call(expected_record)])
        mock_hash.assert_called_once_with('client-token')
        mock_cache.set.assert_has_calls([
            mock.call('client-installation:installation-id', 'record-json', timeout=3600),
            mock.call('client-session:token-hash', 'record-json', timeout=3600),
        ])

    @mock.patch.object(ClientSessionService, '_hash', return_value='challenge-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.json.dumps', return_value='challenge-record')
    @mock.patch('src.client.service.secrets.token_urlsafe', return_value='challenge-token')
    def test_should_create_challenge_and_store_record(
            self, mock_token, mock_dumps, mock_cache, mock_hash
    ):
        actual = ClientSessionService.create_challenge(
            'installation-id', 'public-key', 'web'
        )

        self.assertEqual('challenge-token', actual)
        mock_token.assert_called_once_with(32)
        mock_dumps.assert_called_once_with({
            'installation_id': 'installation-id',
            'public_key': 'public-key',
            'platform': 'web',
        })
        mock_hash.assert_called_once_with('challenge-token')
        mock_cache.set.assert_called_once_with(
            'client-challenge:challenge-hash',
            'challenge-record',
            timeout=300,
        )

    @mock.patch('src.client.service.hashlib.sha256')
    def test_should_hash_token_with_sha256(self, mock_sha256):
        mock_digest = mock_sha256.return_value
        mock_digest.hexdigest.return_value = 'digest'

        actual = ClientSessionService._hash('token')

        self.assertEqual('digest', actual)
        mock_sha256.assert_called_once_with(b'token')
        mock_digest.hexdigest.assert_called_once_with()

    @mock.patch.object(SecurityException, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, '_hash', return_value='challenge-hash')
    @mock.patch.object(Caching, 'CACHE')
    def test_should_raise_security_error_for_missing_challenge(
            self, mock_cache, mock_hash, mock_exception
    ):
        mock_cache.get.return_value = None

        with self.assertRaises(SecurityException):
            ClientSessionService.create_from_challenge(
                'installation-id', 'ios', 'challenge-token', 'signature'
            )

        mock_exception.assert_called_once_with('Challenge', 'Expired or invalid challenge')
        mock_hash.assert_called_once_with('challenge-token')
        mock_cache.get.assert_called_once_with('client-challenge:challenge-hash')

    @mock.patch.object(SecurityException, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, '_hash', return_value='challenge-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'other-installation',
        'public_key': 'encoded-key',
        'platform': 'ios',
    })
    def test_should_raise_security_error_for_wrong_challenge_installation(
            self, mock_loads, mock_cache, mock_hash, mock_exception
    ):
        mock_cache.get.return_value = 'challenge-record'

        with self.assertRaises(SecurityException):
            ClientSessionService.create_from_challenge(
                'installation-id', 'ios', 'challenge-token', 'signature'
            )

        mock_loads.assert_called_once_with('challenge-record')
        mock_exception.assert_called_once_with('Challenge', 'Invalid installation')
        mock_cache.delete.assert_not_called()

    @mock.patch.object(ClientSessionService, 'create', return_value=('token', 2000))
    @mock.patch.object(ClientSessionService, '_hash', return_value='challenge-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.serialization.load_der_public_key',
                side_effect=ValueError)
    @mock.patch('src.client.service.base64.b64decode', side_effect=[b'public-key', b'signature'])
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'public_key': 'encoded-key',
        'platform': 'ios',
    })
    def test_should_use_encoded_point_when_der_key_loading_fails(
            self, mock_loads, mock_b64decode, mock_load_key,
            mock_cache, mock_hash, mock_create
    ):
        public_key = mock.Mock()
        fake_key_type = type(public_key)
        fake_key_type.from_encoded_point = mock.Mock(return_value=public_key)
        mock_cache.get.return_value = 'challenge-record'

        with mock.patch('src.client.service.ec.EllipticCurvePublicKey', fake_key_type), \
            mock.patch('src.client.service.ec.ECDSA', return_value='ecdsa'), \
                mock.patch('src.client.service.hashes.SHA256', return_value='sha256'):
            actual = ClientSessionService.create_from_challenge(
                'installation-id', 'ios', 'challenge-token', 'signature'
            )

        self.assertEqual(('token', 2000), actual)
        fake_key_type.from_encoded_point.assert_called_once_with(
            mock.ANY, b'public-key'
        )
        public_key.verify.assert_called_once()
        mock_cache.delete.assert_called_once_with('client-challenge:challenge-hash')
        mock_create.assert_called_once_with('installation-id', 'encoded-key', 'ios')

    @mock.patch.object(SecurityException, '__init__', return_value=None)
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch.object(ClientSessionService, '_hash', return_value='challenge-hash')
    @mock.patch('src.client.service.json.loads', side_effect=KeyError('public_key'))
    def test_should_raise_security_error_for_invalid_challenge_record(
            self, mock_loads, mock_hash, mock_cache, mock_exception
    ):
        mock_cache.get.return_value = 'challenge-record'

        with self.assertRaises(SecurityException):
            ClientSessionService.create_from_challenge(
                'installation-id', 'ios', 'challenge-token', 'signature'
            )

        mock_exception.assert_called_once_with('Signature', 'Invalid client signature')
        mock_cache.delete.assert_not_called()

    @mock.patch.object(SecurityException, '__init__', return_value=None)
    @mock.patch.object(ClientSessionService, 'create')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch.object(ClientSessionService, '_hash', return_value='challenge-hash')
    @mock.patch('src.client.service.serialization.load_der_public_key',
                return_value=object())
    @mock.patch('src.client.service.base64.b64decode', return_value=b'public-key')
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'public_key': 'encoded-key',
        'platform': 'ios',
    })
    def test_should_raise_security_error_for_non_ec_challenge_key(
            self, mock_loads, mock_b64decode, mock_load_key, mock_hash,
            mock_cache, mock_create, mock_exception
    ):
        mock_cache.get.return_value = 'challenge-record'

        with self.assertRaises(SecurityException):
            ClientSessionService.create_from_challenge(
                'installation-id', 'ios', 'challenge-token', 'signature'
            )

        mock_load_key.assert_called_once_with(b'public-key')
        mock_exception.assert_called_once_with('Signature', 'Invalid client signature')
        mock_create.assert_not_called()
        mock_cache.delete.assert_not_called()

    @mock.patch.object(ClientSessionService, 'create', return_value=('token', 2000))
    @mock.patch.object(ClientSessionService, '_hash', return_value='challenge-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.ec.ECDSA', return_value='ecdsa')
    @mock.patch('src.client.service.hashes.SHA256', return_value='sha256')
    @mock.patch('src.client.service.serialization.load_der_public_key')
    @mock.patch('src.client.service.base64.b64decode', side_effect=[b'public-key', b'signature'])
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'public_key': 'encoded-key',
        'platform': 'ios',
    })
    def test_should_verify_challenge_delete_it_and_create_session(
            self, mock_loads, mock_b64decode, mock_load_key, mock_sha256,
            mock_ecdsa, mock_cache, mock_hash, mock_create
    ):
        public_key = mock.Mock()
        mock_load_key.return_value = public_key
        fake_key_type = type(public_key)

        with mock.patch('src.client.service.ec.EllipticCurvePublicKey', fake_key_type):
            mock_cache.get.return_value = 'challenge-record'
            actual = ClientSessionService.create_from_challenge(
                'installation-id', 'ios', 'challenge-token', 'signature'
            )

        self.assertEqual(('token', 2000), actual)
        mock_cache.get.assert_called_once_with('client-challenge:challenge-hash')
        mock_loads.assert_called_once_with('challenge-record')
        mock_b64decode.assert_has_calls([
            mock.call('encoded-key', validate=True),
            mock.call('signature', validate=True),
        ])
        public_key.verify.assert_called_once_with(
            b'signature', b'challenge-token', 'ecdsa'
        )
        mock_cache.delete.assert_called_once_with('client-challenge:challenge-hash')
        mock_create.assert_called_once_with(
            'installation-id', 'encoded-key', 'ios'
        )

    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch.object(Caching, 'CACHE')
    def test_should_return_false_when_token_is_missing(self, mock_cache, mock_hash):
        mock_cache.get.return_value = None

        actual = ClientSessionService.validate('token')

        self.assertFalse(actual)
        mock_hash.assert_called_once_with('token')
        mock_cache.get.assert_called_once_with('client-session:token-hash')

    @mock.patch('src.client.service.time.time', return_value=1000)
    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.json.loads', return_value={'expires_at': 1001})
    def test_should_return_true_for_unexpired_token(
            self, mock_loads, mock_cache, mock_hash, mock_time
    ):
        mock_cache.get.return_value = 'record-json'

        actual = ClientSessionService.validate('token')

        self.assertTrue(actual)
        mock_loads.assert_called_once_with('record-json')
        mock_time.assert_called_once_with()

    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.json.loads', return_value={'expires_at': 1000})
    @mock.patch('src.client.service.time.time', return_value=1000)
    def test_should_return_false_for_expired_token(
            self, mock_time, mock_loads, mock_cache, mock_hash
    ):
        mock_cache.get.return_value = 'record-json'

        actual = ClientSessionService.validate('token')

        self.assertFalse(actual)
        mock_loads.assert_called_once_with('record-json')
        mock_time.assert_called_once_with()

    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.json.loads', side_effect=ValueError)
    def test_should_return_false_for_malformed_token_record(
            self, mock_loads, mock_cache, mock_hash
    ):
        mock_cache.get.return_value = 'malformed-record'

        actual = ClientSessionService.validate('token')

        self.assertFalse(actual)
        mock_loads.assert_called_once_with('malformed-record')

    @mock.patch.object(ClientSessionService, '_hash', return_value='request-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.ec.ECDSA', return_value='ecdsa')
    @mock.patch('src.client.service.hashes.SHA256', return_value='sha256')
    @mock.patch('src.client.service.serialization.load_der_public_key')
    @mock.patch('src.client.service.base64.b64decode', side_effect=[b'public-key', b'signature'])
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'platform': 'ios',
        'expires_at': 1100,
        'public_key': 'encoded-key',
    })
    @mock.patch('src.client.service.hashlib.sha256')
    @mock.patch('src.client.service.time.time', return_value=1000)
    def test_should_authenticate_request_and_add_replay_key(
            self, mock_time, mock_sha256, mock_loads, mock_b64decode,
            mock_load_key, mock_sha256_algorithm, mock_ecdsa, mock_cache, mock_hash
    ):
        public_key = mock.Mock()
        mock_load_key.return_value = public_key
        mock_sha256.return_value.hexdigest.return_value = 'body-hash'
        mock_cache.get.return_value = 'record-json'
        mock_cache.add.return_value = True
        fake_key_type = type(public_key)

        with mock.patch('src.client.service.ec.EllipticCurvePublicKey', fake_key_type):
            actual = ClientSessionService.authenticate_request(
                'token', 'installation-id', 'ios', '1000', 'request-id',
                'signature', 'post', '/path', b'body'
            )

        self.assertTrue(actual)
        mock_cache.add.assert_called_once_with(
            'client-request:request-hash', '1', timeout=300
        )
        public_key.verify.assert_called_once_with(
            b'signature',
            b'POST\n/path\n1000\nrequest-id\nbody-hash\nios\ninstallation-id',
            'ecdsa',
        )

    @mock.patch.object(ClientSessionService, '_hash', return_value='request-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.ec.ECDSA', return_value='ecdsa')
    @mock.patch('src.client.service.hashes.SHA256', return_value='sha256')
    @mock.patch('src.client.service.serialization.load_der_public_key',
                side_effect=ValueError)
    @mock.patch('src.client.service.base64.b64decode', side_effect=[b'public-key', b'signature'])
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'platform': 'ios',
        'expires_at': 1100,
        'public_key': 'encoded-key',
    })
    @mock.patch('src.client.service.hashlib.sha256')
    @mock.patch('src.client.service.time.time', return_value=1000)
    def test_should_authenticate_with_encoded_point_when_der_key_loading_fails(
            self, mock_time, mock_sha256, mock_loads, mock_b64decode,
            mock_load_key, mock_sha256_algorithm, mock_ecdsa, mock_cache, mock_hash
    ):
        public_key = mock.Mock()
        fake_key_type = type(public_key)
        fake_key_type.from_encoded_point = mock.Mock(return_value=public_key)
        mock_sha256.return_value.hexdigest.return_value = 'body-hash'
        mock_cache.get.return_value = 'record-json'
        mock_cache.add.return_value = True

        with mock.patch('src.client.service.ec.EllipticCurvePublicKey', fake_key_type):
            actual = ClientSessionService.authenticate_request(
                'token', 'installation-id', 'ios', '1000', 'request-id',
                'signature', 'post', '/path', b'body'
            )

        self.assertTrue(actual)
        fake_key_type.from_encoded_point.assert_called_once_with(
            mock.ANY, b'public-key'
        )
        public_key.verify.assert_called_once()
        mock_cache.add.assert_called_once_with(
            'client-request:request-hash', '1', timeout=300
        )

    @mock.patch.object(ClientSessionService, '_hash', return_value='request-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.time.time', return_value=1000)
    def test_should_store_replay_key_when_cache_has_no_add(
            self, mock_time, mock_cache, mock_hash
    ):
        del mock_cache.add
        mock_cache.get.side_effect = ['record-json', None]
        mock_cache.set.return_value = True

        with mock.patch('src.client.service.json.loads', return_value={
                'installation_id': 'installation-id',
                'platform': 'ios',
                'expires_at': 1100,
                'public_key': 'encoded-key',
        }), mock.patch('src.client.service.serialization.load_der_public_key') as mock_load_key:
            public_key = mock.Mock()
            mock_load_key.return_value = public_key
            fake_key_type = type(public_key)
            with mock.patch('src.client.service.ec.EllipticCurvePublicKey', fake_key_type), \
                    mock.patch('src.client.service.base64.b64decode', side_effect=[b'key', b'signature']), \
                    mock.patch('src.client.service.ec.ECDSA', return_value='ecdsa'), \
                    mock.patch('src.client.service.hashes.SHA256', return_value='sha256'), \
                    mock.patch('src.client.service.hashlib.sha256') as mock_sha256:
                mock_sha256.return_value.hexdigest.return_value = 'body-hash'
                actual = ClientSessionService.authenticate_request(
                    'token', 'installation-id', 'ios', '1000', 'request-id',
                    'signature', 'post', '/path', b'body'
                )

        self.assertTrue(actual)
        mock_cache.set.assert_called_once_with(
            'client-request:request-hash', '1', timeout=300
        )

    @mock.patch('src.client.service.time.time', return_value=1000)
    def test_should_reject_stale_authenticated_request_without_cache_access(
            self, mock_time
    ):
        with mock.patch.object(Caching, 'CACHE') as mock_cache:
            actual = ClientSessionService.authenticate_request(
                'token', 'installation-id', 'ios', '0', 'request-id',
                'signature', 'post', '/path', b'body'
            )

        self.assertFalse(actual)
        mock_time.assert_called_once_with()
        mock_cache.get.assert_not_called()

    @mock.patch.object(Caching, 'CACHE')
    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    def test_should_reject_authenticated_request_when_token_is_missing(
            self, mock_hash, mock_cache
    ):
        mock_cache.get.return_value = None

        with mock.patch('src.client.service.time.time', return_value=1000):
            actual = ClientSessionService.authenticate_request(
                'token', 'installation-id', 'ios', '1000', 'request-id',
                'signature', 'post', '/path', b'body'
            )

        self.assertFalse(actual)
        mock_cache.get.assert_called_once_with('client-session:token-hash')

    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.time.time', return_value=1000)
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'other-installation',
        'platform': 'ios',
        'expires_at': 1100,
        'public_key': 'encoded-key',
    })
    def test_should_reject_authenticated_request_for_wrong_installation(
            self, mock_loads, mock_time, mock_cache, mock_hash
    ):
        mock_cache.get.return_value = 'record-json'

        actual = ClientSessionService.authenticate_request(
            'token', 'installation-id', 'ios', '1000', 'request-id',
            'signature', 'post', '/path', b'body'
        )

        self.assertFalse(actual)
        mock_loads.assert_called_once_with('record-json')

    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.time.time', return_value=1000)
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'platform': 'other-platform',
        'expires_at': 1100,
        'public_key': 'encoded-key',
    })
    def test_should_reject_authenticated_request_for_wrong_platform(
            self, mock_loads, mock_time, mock_cache, mock_hash
    ):
        mock_cache.get.return_value = 'record-json'

        actual = ClientSessionService.authenticate_request(
            'token', 'installation-id', 'ios', '1000', 'request-id',
            'signature', 'post', '/path', b'body'
        )

        self.assertFalse(actual)

    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.time.time', return_value=1000)
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'platform': 'ios',
        'expires_at': 1000,
        'public_key': 'encoded-key',
    })
    def test_should_reject_authenticated_request_for_expired_session(
            self, mock_loads, mock_time, mock_cache, mock_hash
    ):
        mock_cache.get.return_value = 'record-json'

        actual = ClientSessionService.authenticate_request(
            'token', 'installation-id', 'ios', '1000', 'request-id',
            'signature', 'post', '/path', b'body'
        )

        self.assertFalse(actual)

    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.serialization.load_der_public_key',
                return_value=object())
    @mock.patch('src.client.service.base64.b64decode', return_value=b'key')
    @mock.patch('src.client.service.time.time', return_value=1000)
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'platform': 'ios',
        'expires_at': 1100,
        'public_key': 'encoded-key',
    })
    def test_should_reject_authenticated_request_for_non_ec_key(
            self, mock_loads, mock_time, mock_b64decode, mock_load_key,
            mock_cache, mock_hash
    ):
        mock_cache.get.return_value = 'record-json'

        actual = ClientSessionService.authenticate_request(
            'token', 'installation-id', 'ios', '1000', 'request-id',
            'signature', 'post', '/path', b'body'
        )

        self.assertFalse(actual)
        mock_load_key.assert_called_once_with(b'key')

    @mock.patch.object(Caching, 'CACHE')
    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch('src.client.service.time.time', return_value=1000)
    @mock.patch('src.client.service.json.loads', side_effect=KeyError('platform'))
    def test_should_return_false_for_invalid_authenticated_record(
            self, mock_loads, mock_time, mock_hash, mock_cache
    ):
        mock_cache.get.return_value = 'record-json'

        actual = ClientSessionService.authenticate_request(
            'token', 'installation-id', 'ios', '1000', 'request-id',
            'signature', 'post', '/path', b'body'
        )

        self.assertFalse(actual)
        mock_loads.assert_called_once_with('record-json')
        mock_cache.add.assert_not_called()

    @mock.patch.object(Caching, 'CACHE')
    @mock.patch.object(ClientSessionService, '_hash', return_value='token-hash')
    @mock.patch('src.client.service.time.time', return_value=1000)
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'platform': 'ios',
        'expires_at': 1100,
        'public_key': 'encoded-key',
    })
    @mock.patch('src.client.service.base64.b64decode', side_effect=ValueError)
    def test_should_return_false_for_invalid_authenticated_key_encoding(
            self, mock_b64decode, mock_loads, mock_time, mock_hash, mock_cache
    ):
        mock_cache.get.return_value = 'record-json'

        actual = ClientSessionService.authenticate_request(
            'token', 'installation-id', 'ios', '1000', 'request-id',
            'signature', 'post', '/path', b'body'
        )

        self.assertFalse(actual)
        mock_b64decode.assert_called_once_with('encoded-key', validate=True)
        mock_cache.add.assert_not_called()

    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.time.time', return_value=1000)
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'platform': 'ios',
        'expires_at': 1100,
        'public_key': 'encoded-key',
    })
    def test_should_return_false_for_invalid_request_signature(
            self, mock_loads, mock_time, mock_cache
    ):
        mock_cache.get.return_value = 'record-json'
        public_key = mock.Mock()
        public_key.verify.side_effect = InvalidSignature

        with mock.patch('src.client.service.serialization.load_der_public_key',
                        return_value=public_key), \
                mock.patch('src.client.service.ec.EllipticCurvePublicKey', type(public_key)), \
                mock.patch('src.client.service.base64.b64decode', side_effect=[b'key', b'signature']), \
                mock.patch('src.client.service.ec.ECDSA', return_value='ecdsa'), \
                mock.patch('src.client.service.hashes.SHA256', return_value='sha256'), \
                mock.patch('src.client.service.hashlib.sha256') as mock_sha256:
            mock_sha256.return_value.hexdigest.return_value = 'body-hash'
            actual = ClientSessionService.authenticate_request(
                'token', 'installation-id', 'ios', '1000', 'request-id',
                'signature', 'post', '/path', b'body'
            )

        self.assertFalse(actual)
        mock_cache.add.assert_not_called()
        mock_cache.set.assert_not_called()

    @mock.patch.object(ClientSessionService, '_hash', return_value='request-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.ec.ECDSA', return_value='ecdsa')
    @mock.patch('src.client.service.hashes.SHA256', return_value='sha256')
    @mock.patch('src.client.service.serialization.load_der_public_key')
    @mock.patch('src.client.service.base64.b64decode', side_effect=[b'key', b'signature'])
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'platform': 'ios',
        'expires_at': 1100,
        'public_key': 'encoded-key',
    })
    @mock.patch('src.client.service.hashlib.sha256')
    @mock.patch('src.client.service.time.time', return_value=1000)
    def test_should_return_false_when_replay_cache_add_rejects_request(
            self, mock_time, mock_sha256, mock_loads, mock_b64decode,
            mock_load_key, mock_sha256_algorithm, mock_ecdsa, mock_cache, mock_hash
    ):
        public_key = mock.Mock()
        mock_load_key.return_value = public_key
        mock_sha256.return_value.hexdigest.return_value = 'body-hash'
        mock_cache.get.return_value = 'record-json'
        mock_cache.add.return_value = False
        fake_key_type = type(public_key)

        with mock.patch('src.client.service.ec.EllipticCurvePublicKey', fake_key_type):
            actual = ClientSessionService.authenticate_request(
                'token', 'installation-id', 'ios', '1000', 'request-id',
                'signature', 'post', '/path', b'body'
            )

        self.assertFalse(actual)
        mock_cache.add.assert_called_once_with(
            'client-request:request-hash', '1', timeout=300
        )

    @mock.patch.object(ClientSessionService, '_hash', return_value='request-hash')
    @mock.patch.object(Caching, 'CACHE')
    @mock.patch('src.client.service.ec.ECDSA', return_value='ecdsa')
    @mock.patch('src.client.service.hashes.SHA256', return_value='sha256')
    @mock.patch('src.client.service.serialization.load_der_public_key')
    @mock.patch('src.client.service.base64.b64decode', side_effect=[b'key', b'signature'])
    @mock.patch('src.client.service.json.loads', return_value={
        'installation_id': 'installation-id',
        'platform': 'ios',
        'expires_at': 1100,
        'public_key': 'encoded-key',
    })
    @mock.patch('src.client.service.hashlib.sha256')
    @mock.patch('src.client.service.time.time', return_value=1000)
    def test_should_return_false_when_replay_key_already_exists(
            self, mock_time, mock_sha256, mock_loads, mock_b64decode,
            mock_load_key, mock_sha256_algorithm, mock_ecdsa, mock_cache, mock_hash
    ):
        del mock_cache.add
        public_key = mock.Mock()
        mock_load_key.return_value = public_key
        mock_sha256.return_value.hexdigest.return_value = 'body-hash'
        mock_cache.get.side_effect = ['record-json', 'existing-replay-key']
        fake_key_type = type(public_key)

        with mock.patch('src.client.service.ec.EllipticCurvePublicKey', fake_key_type):
            actual = ClientSessionService.authenticate_request(
                'token', 'installation-id', 'ios', '1000', 'request-id',
                'signature', 'post', '/path', b'body'
            )

        self.assertFalse(actual)
        mock_cache.set.assert_not_called()
