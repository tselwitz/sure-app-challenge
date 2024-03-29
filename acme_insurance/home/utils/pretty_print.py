from uuid import UUID
from decimal import Decimal
from home.utils.rounding import limit_decimal_places


class PrettyPrint:
    def create_fields_dict(self):
        fields_dict = {}
        for field in self._meta.fields:
            attr = getattr(self, field.name)
            if isinstance(attr, (bool, str, int, float, UUID)):
                fields_dict[field.name] = attr
            elif isinstance(attr, Decimal):
                fields_dict[field.name] = limit_decimal_places(attr, places=3)
            else:
                fields_dict[field.name] = attr.pretty_print()
        return fields_dict

    def pretty_print(self) -> dict:
        return self.create_fields_dict()

    def __str__(self) -> str:
        fields_dict = {
            field.name: getattr(self, field.name) for field in self._meta.fields
        }
        return str(fields_dict)
