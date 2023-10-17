from django.db import models
from django.db import models
from uuid import uuid4
from home.utils.pretty_print import PrettyPrint


class State(PrettyPrint, models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    state = models.CharField(max_length=50)

    tax_multiplier = models.FloatField(default=1.0)
    flood_multiplier = models.FloatField(default=1.0)
