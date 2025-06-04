from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from Product.models import Product, Cart
# Create your views here.

# @login_required(login_url='registration')
def home(request):
    # Get products marked as featured (or any other condition you want)
    featured_products = Product.objects.filter(featured=True, in_stock=True, image__isnull=False)[:6]
    new_arrival = Product.objects.filter(new_arrival=True) 
    top_rated = Product.objects.filter(top_rated=True)
    featured = Product.objects.filter(featured=True)

    cart_items = Cart.objects.filter(user=request.user.username) if request.user.is_authenticated else []

    return render(request, 'home/home.html', {'featured_products': featured_products, 'new_arrival': new_arrival, 'top_rated': top_rated, 'featured':featured, 'cart_items': cart_items,})

def shop(request):
    all_product = Product.objects.all()
    cart_items = Cart.objects.filter(user=request.user.username) if request.user.is_authenticated else []

    return render(request, 'home/shop.html', {'all_product': all_product, 'cart_items': cart_items})


def single_product(request, id):
    # Get the main product
    product = get_object_or_404(Product, id=id)
    
    # Get related products (for example, based on the same category)
    related_products = Product.objects.all().exclude(id=product.id)[:8]
    # related_products = Product.objects.filter(category=product.category).exclude(id=product.id).distinct()[:8]
    # related_products = Product.objects.filter(category=product.category).exclude(id=product.id).distinct().order_by('?')[:8]
    cart_items = Cart.objects.filter(user=request.user.username) if request.user.is_authenticated else []

    return render(request, 'home/single_product.html', {
        'product': product,
        'related_products': related_products,
        'cart_items': cart_items,
    })


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(user = request.user, product=product)
        cart.quantity += 1
        cart.save()
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user.username, product=product)
        cart.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def checkout(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user.username)
    else:
        cart_items = []

    # Calculate grand total
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'home/checkout.html', {
        'cart_items': cart_items,
        'cart_total': total
    })