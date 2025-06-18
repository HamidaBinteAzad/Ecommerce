from .models import Cart
def cart_product(request):
    items = Cart.objects.filter(user = request.user)
    return {'cart_items': items}