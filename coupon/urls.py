from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('coupon_action<int:id>',views.coupon_action,name='coupon_action'),
    path('check_coupon_validity',views.check_coupon_validity,name='check_coupon_validity'),
    path('coupon_cancel',views.coupon_cancel,name='coupon_cancel')
   
]