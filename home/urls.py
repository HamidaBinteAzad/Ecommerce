from django.urls import path
from . views import home,shop, single_product, add_to_cart, decrement_cart, view_cart, checkout, payment, payment_success, payment_cancel, payment_fail

urlpatterns = [
    path("", home, name='home'),
    path("shop/", shop, name='shop'),
    path('single_product/<int:id>/', single_product, name='single_product'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('dec/<int:cart_id>/', decrement_cart, name='decrement_cart'),   
    path('cart/', view_cart, name='view_cart'),   
    path('checkout/', checkout, name='checkout'),
    path('payment/', payment, name='payment'),
    path('payment/success/', payment_success, name='success'),
    path('payment/fail/', payment_fail, name='fail'),
    path('payment/cancel/', payment_cancel, name='cancel'),
]