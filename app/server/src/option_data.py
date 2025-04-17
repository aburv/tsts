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

    @staticmethod
    def get_id_types() -> dict:
        """
        :return: user id types
        :rtype: list
        """
        return {"P": "Phone", "M": "Mail"}

    @staticmethod
    def get_resources() -> dict:
        """
        :return: resources
        :rtype: list
        """
        return {"U": "User", "I": "Image"}

    @staticmethod
    def get_permissions() -> dict:
        """
        :return: permissions
        :rtype: list
        """
        return {"V": "View", "E": "Edit", "C": "Create"}
