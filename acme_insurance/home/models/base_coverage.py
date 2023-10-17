from django.db import models
from django.db import models
from uuid import uuid4
from home.utils.pretty_print import PrettyPrint


class Base_Coverage(PrettyPrint, models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    base_coverage_type = models.CharField(max_length=100)
    price = models.FloatField()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, __value: object) -> bool:
        if self.id == __value.id:
            return True
        elif (
            self.base_coverage_type == __value.base_coverage_type
            and self.price == __value.price
        ):
            return True
        else:
            return False
