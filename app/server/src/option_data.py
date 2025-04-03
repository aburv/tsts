"""
App Options Data
"""


class OptionData:
    """
    Data
    """

    @staticmethod
    def get_platforms() -> dict:
        """
        :return: platforms
        :rtype: list
        """
        return {"A": "App", "B": "Browser"}

    @staticmethod
    def get_device_types() -> dict:
        """
        :return: Device types
        :rtype: list
        """
        return {"D": "Desktop", "P": "Phone", "T": "Tab"}
