import unittest

from src.user.service import UserServices


class DUserServiceTest(unittest.TestCase):

    def test_should_return_empty_dict_on_get_user_data(self):
        service = UserServices()
        expected = {}

        actual = service.get_user_data('data')

        self.assertEqual(actual, expected)
