from django.db import models
from django.db import models
from uuid import uuid4
from home.utils.pretty_print import PrettyPrint


class Additional_Costs(PrettyPrint, models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, __value: object) -> bool:
        if self.id == __value.id:
            return True
        elif self.description == __value.description and self.price == __value.price:
            return True
        else:
            return False
