from django.urls import path
from cart import views


urlpatterns = [
    path("cart_page", views.Cart, name="Cart"),
    path("add_cart<int:id>/", views.add_cart, name="add_cart"),
    path("delete_cart<int:id>", views.delete_cart, name="delete_cart"),
    path("quantity_cart", views.quantity_cart, name="quantity_cart"),
    path("wishlist_page", views.wishlist_page, name="wishlist_page"),
    path("wishlist_new<int:id>", views.wishlist_new, name="wishlist_new"),
    path("wishlist_to_cart", views.add_to_cart, name="add_to_cart"),
    path("wishlist_remove", views.wishlist_remove, name="wishlist_remove"),
    # path('minus_cart<int:id>/<int:price>',views.minus_cart,name='minus_cart'),
]
