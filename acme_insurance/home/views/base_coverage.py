from home.models.base_coverage import Base_Coverage
from home.utils.api_crud import API_CRUD


class Base_Coverage_View(API_CRUD):
    def __init__(self, *args, **kwargs):
        return super().__init__(Base_Coverage, *args, **kwargs)
