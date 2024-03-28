from django.urls import path
from . import views


urlpatterns = [
    path("product_offer", views.product_offer, name="product_offer"),
    path("add_product_offer", views.add_product_offer, name="add_product_offer"),
    path(
        "product_offer_action<int:id>",
        views.product_offer_action,
        name="product_offer_action",
    ),
    path("category_offer", views.category_offer, name="category_offer"),
    path("add_category_offer", views.add_category_offer, name="add_category_offer"),
    path(
        "category_offer_action<int:id>",
        views.category_offer_action,
        name="category_offer_action",
    ),
    path(
        "edit_product_offer<int:id>",
        views.edit_product_offer,
        name="edit_product_offer",
    ),
    path(
        "edit_category_offer<int:id>",
        views.edit_category_offer,
        name="edit_category_offer",
    ),
]
