from home.models.additional_costs import Additional_Costs
from home.utils.api_crud import API_CRUD


class Additional_Costs_View(API_CRUD):
    def __init__(self, *args, **kwargs):
        return super().__init__(Additional_Costs, *args, **kwargs)
