from home.models.state import State
from home.utils.api_crud import API_CRUD


class State_View(API_CRUD):
    def __init__(self, *args, **kwargs):
        return super().__init__(State, *args, **kwargs)
