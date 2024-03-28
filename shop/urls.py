from django.urls import path
from shop import views


urlpatterns = [
    path("shop/", views.shop, name="shop"),
    path("shop_search/", views.shop_search, name="shop_search"),
    # path("shop_filter/", views.shop_filter, name="shop_filter"),
    # path("shop_cat<int:id>/", views.shop_cat, name="shop_cat"),
    path("single_prodect<int:id>", views.single_prodect, name="single_prodect"),
    path(
        "single_prodect_img/<int:id>/<int:img>",
        views.single_prodect_img,
        name="single_prodect_img",
    ),
    # path('wishlist<int:id>',views.wishlist,name='wishlist'),
    path("wishlist/<int:id>/", views.wishlist, name="wishlist"),
]
