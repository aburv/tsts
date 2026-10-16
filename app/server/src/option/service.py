"""
data option service
"""
from src.db_duo import PostgresDbDuo
from src.option.data import FormOptionData, FormType, OptionData, OptionDataFilterType


class OptionService:
    """
    Form Option Services
    """

    def __init__(self, form: FormType):
        self._data = FormOptionData(form)
        self._db = PostgresDbDuo(self._data)

    def get_options(self) -> dict:
        """
        get options by form type
        """

        records = self._db.get_records()
        data = {}
        for record in records:
            field_type = self.get_field_key(record["a.field"])
            try:
                data[field_type].append({
                    "id": record["b.id"],
                    "value": record["b.f_value"]
                })
            except KeyError:
                data[field_type] = [{
                    "id": record["b.id"],
                    "value": record["b.f_value"]
                }]

        return data

    @staticmethod
    def get_field_key(field) -> str:
        """
        get field key
        """
        if '_' not in field:
            return field.lower()
        words = field.split('_')
        return words[0].lower()[0] + ''.join(word.capitalize() for word in words[1:])


class OptionValueService:
    """
    Option Services
    """

    def __init__(self):
        self._data = OptionData()
        self._db = PostgresDbDuo(self._data)

    def get_option_value_by_ids(self, ids: list) -> dict:
        """
        get options by form type
        """
        self._data.on_select({"valueId": ids}, OptionDataFilterType.ID)
        records = self._db.get_records()
        data = {}
        for record in records:
            data[record["id"]] = record["f_value"]
        return data
