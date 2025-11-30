import unittest
from unittest import mock

from src.player.service import PlayerServices
from src.player_gear.service import PlayerGearServices
from src.search.service import SearchServices
from src.user.service import UserServices


class SearchServiceTest(unittest.TestCase):

    @mock.patch.object(PlayerServices, "__init__", return_value=None)
    @mock.patch.object(PlayerServices, "search_by_name", return_value=["player_id_1"])
    @mock.patch.object(PlayerGearServices, "__init__", return_value=None)
    @mock.patch.object(PlayerGearServices, "search_by_j_name_j_no", return_value=["player_id_2"])
    @mock.patch.object(UserServices, "__init__", return_value=None)
    @mock.patch.object(UserServices, "get_users_by_player_ids_and_text", return_value=[])
    def test_should_return_empty_list_on_search(self,
                                                mock_get_users_by_player_ids_and_text,
                                                mock_user_services,
                                                mock_search_by_j_name_j_no,
                                                mock_player_gear_services,
                                                mock_search_by_name,
                                                mock_player_services
                                                ):
        actual = SearchServices.search("text", "u_id")

        mock_user_services.assert_called_once_with()
        mock_search_by_name.assert_called_once_with("text", "u_id")
        mock_player_gear_services.assert_called_once_with()
        mock_search_by_j_name_j_no.assert_called_once_with("text", "u_id")
        mock_player_services.assert_called_once_with()
        mock_get_users_by_player_ids_and_text.assert_called_once_with(['player_id_1', 'player_id_2'], "text")

        self.assertEqual(actual, {'player': []})
