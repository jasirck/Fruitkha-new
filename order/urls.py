from django.urls import path
from order import views


urlpatterns = [
    path('checkout',views.checkout,name='checkout'),
    path('chenge<int:id>',views.chenge,name='chenge'),
    path('add_address_order',views.add_address_order,name='add_address_order'),
    path('cod_order',views.cod_order,name='cod_order'),
    path('succes',views.succes,name='succes'),
    path('proceed_to_pay',views.razorpaychek),
    path('online_order/',views.online_order,name='online_order'),
    path('online_sucess/',views.online_sucess,name="online_sucess"),
    path('address_check<int:id>/<int:a_id>',views.address_check,name='address_check'),
    
]