from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("my_admin", views.admin_login, name="admin_login"),
    path("admin_logout", views.admin_logout, name="admin_logout"),
    path("dashboard", views.dashbord, name="dashboard"),
    path("management", views.management, name="management"),
    path("add_prodect", views.add_prodect, name="add_prodect"),
    path("edit_prodect", views.edit_prodect, name="edit_prodect"),
    path("category", views.category, name="category"),
    path("category_deleted", views.category_deleted, name="category_deleted"),
    path("readd_category<int:id>", views.readd_category, name="readd_category"),
    path("variant", views.variant, name="variant"),
    path("orders", views.orders, name="orders"),
    path("orders_deteils_admin<int:id>", views.orders_deteils, name="orders_deteils"),
    path("edit_category", views.edit_category, name="edit_category"),
    path("delete_category<int:id>", views.delete_category, name="delete_category"),
    path("delete_variant<int:id>", views.delete_variant, name="delete_variant"),
    path("edit_variant", views.edit_variant, name="edit_variant"),
    path(
        "edit_category_page<int:id>",
        views.edit_category_page,
        name="edit_category_page",
    ),
    path("deleted", views.deleted, name="deleted"),
    path("action<int:id>", views.action, name="action"),
    path("unlist<int:id>", views.unlist, name="unlist"),
    path("delete<int:id>", views.delete, name="delete"),
    path("readd<int:id>", views.readd, name="readd"),
    path(
        "edit_prodect_page<int:id>", views.edit_prodect_page, name="edit_prodect_page"
    ),
    path(
        "order_back_pending<int:id>",
        views.order_back_pending,
        name="order_back_pending",
    ),
    path("orders_deliverd<int:id>", views.orders_deliverd, name="orders_deliverd"),
    path("orders_cancel<int:id>", views.orders_cancel, name="orders_cancel"),
    path("return_accept<int:id>", views.return_accept, name="return_accept"),
    path("coupon", views.coupon, name="coupon"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
