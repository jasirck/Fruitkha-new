from django.urls import path
from . import views


urlpatterns = [
    path("wallet", views.wallet, name="wallet"),
    path("return_order<int:id>", views.return_order, name="return_order"),
]
