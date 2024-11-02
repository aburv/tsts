"""
User Service
"""


class SearchServices:
    """
    Data Search
    """

    @staticmethod
    def search(text: str) -> list:
        """
        :return:
        :rtype:
        """
        # Use ILIKE for case-insensitive search
        # cursor.execute("SELECT id, title FROM images WHERE title ILIKE %s OR description ILIKE %s",
        #                (f'%{query}%', f'%{query}%'))

        # results = cursor.fetchall()

        # Format results as a list of dictionaries
        return []
