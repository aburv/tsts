"""
Search Service
"""
from src.player.service import PlayerServices
from src.player_gear.service import PlayerGearServices
from src.user.service import UserServices


class SearchServices:
    """
    Data Search
    """

    @staticmethod
    def search(text: str, u_id: str) -> dict:
        """
        :return:
        :rtype:
        """
        player_ids = PlayerServices().search_by_name(text, u_id)
        player_ids += PlayerGearServices().search_by_j_name_j_no(text, u_id)
        users = []
        if len(player_ids) > 0:
            users = UserServices().get_users_by_player_ids_and_text(player_ids, text)
        data = {
            "player": users
        }
        return data
