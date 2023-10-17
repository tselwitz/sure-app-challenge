from django.urls import path

from home.views.additional_costs import Additional_Costs_View
from home.views.base_coverage import Base_Coverage_View
from home.views.quote import Quote_View
from home.views.state import State_View

urlpatterns = [
    path(
        "additional_costs/",
        Additional_Costs_View.as_view(),
    ),
    path(
        "additional_costs/delete/",
        Additional_Costs_View.as_view(),
    ),
    path("base_coverage/", Base_Coverage_View.as_view()),
    path("base_coverage/delete/", Base_Coverage_View.as_view()),
    path("quote/", Quote_View.as_view()),
    path("quote/delete/", Quote_View.as_view()),
    path("state/", State_View.as_view()),
    path("state/delete/", State_View.as_view()),
]
