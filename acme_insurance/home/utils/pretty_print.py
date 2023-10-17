class PrettyPrint:
    def create_fields_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

    def get_dict(self) -> dict:
        return self.create_fields_dict()

    def __str__(self) -> str:
        fields_dict = {
            field.name: getattr(self, field.name) for field in self._meta.fields
        }
        return str(fields_dict)
