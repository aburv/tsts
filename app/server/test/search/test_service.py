import unittest

from src.search.service import SearchServices


class SearchServiceTest(unittest.TestCase):

    def test_should_return_empty_list_on_search(self):
        actual = SearchServices.search("text", "u_id")

        self.assertEqual(actual, [])
