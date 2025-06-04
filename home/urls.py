from django.urls import path
from . views import home,shop, single_product, add_to_cart, checkout

urlpatterns = [
    path("", home, name='home'),
    path("shop/", shop, name='shop'),
    path('single_product/<int:id>/', single_product, name='single_product'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
]