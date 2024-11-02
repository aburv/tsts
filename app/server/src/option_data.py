"""
App Options Data
"""


class OptionData:
    """
    Data
    """

    @staticmethod
    def get_platforms() -> list:
        """
        :return: platforms
        :rtype: list
        """
        return ["App", "Browser"]

    @staticmethod
    def get_device_types() -> list:
        """
        :return: Device types
        :rtype: list
        """
        return ["Desktop", "Phone", "Tab"]
