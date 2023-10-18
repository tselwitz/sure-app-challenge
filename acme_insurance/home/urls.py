from django.urls import path

from home.views.additional_costs import Additional_Costs_View
from home.views.base_coverage import Base_Coverage_View
from home.views.quote import Quote_View
from home.views.state import State_View

urlpatterns = [
    path(
        "additional_costs/",
        Additional_Costs_View.as_view(),
        name="additional_costs_list_create_delete",
    ),
    path(
        "base_coverage/",
        Base_Coverage_View.as_view(),
        name="base_coverage_list_create_delete",
    ),
    path("quote/", Quote_View.as_view(), name="quote_list_create_delete"),
    path("quote/rater/", Quote_View.as_view(), name="quote_rater"),
    path("state/", State_View.as_view(), name="state_list_create"),
]
