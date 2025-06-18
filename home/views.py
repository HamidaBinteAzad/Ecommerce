from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from Product.models import Product, Cart
from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Create your views here.

# @login_required(login_url='registration')
def home(request):
    # Get products marked as featured (or any other condition you want)
    featured_products = Product.objects.filter(featured=True, in_stock=True, image__isnull=False)[:6]
    new_arrival = Product.objects.filter(new_arrival=True) 
    top_rated = Product.objects.filter(top_rated=True)
    featured = Product.objects.filter(featured=True)

    # cart_items = Cart.objects.filter(user=request.user.username) if request.user.is_authenticated else []

    return render(request, 'home/home.html', {'featured_products': featured_products, 'new_arrival': new_arrival, 'top_rated': top_rated, 'featured':featured,})

def shop(request):
    all_product = Product.objects.all()
    # cart_items = Cart.objects.filter(user=request.user.username) if request.user.is_authenticated else []

    return render(request, 'home/shop.html', {'all_product': all_product,})


def single_product(request, id):
    # Get the main product
    product = get_object_or_404(Product, id=id)
    
    # Get related products (for example, based on the same category)
    related_products = Product.objects.all().exclude(id=product.id)[:8]
    # related_products = Product.objects.filter(category=product.category).exclude(id=product.id).distinct()[:8]
    # related_products = Product.objects.filter(category=product.category).exclude(id=product.id).distinct().order_by('?')[:8]
    # cart_items = Cart.objects.filter(user=request.user.username) if request.user.is_authenticated else []

    return render(request, 'home/single_product.html', {
        'product': product,
        'related_products': related_products,
    })



# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     try:
#         cart = Cart.objects.get(user = request.user, product=product)
#         cart.quantity += 1
#         cart.save(update_fields=['quantity'])
#     except Cart.DoesNotExist:
#         cart = Cart.objects.create(user=request.user.username, product=product)
#         cart.save(update_fields=['quantity'])
#     return redirect(request.META.get('HTTP_REFERER', '/'))

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('registration')  # Require login
    
    product = get_object_or_404(Product, id=product_id)
    username = request.user.username  # Consistent username usage
    
    # Use get_or_create for cleaner code
    cart_item, created = Cart.objects.get_or_create(
        user=username,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

# def view_cart(request):
#     cart_item = Cart.objects.all()
#     return render(request, 'home/view_cart.html', {
#         'cart_items': cart_item
#     })

def view_cart(request):
    # Only show current user's cart
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user.username)
        # Calculate total
        total = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total = 0
    
    return render(request, 'home/view_cart.html', {
        'cart_items': cart_items,
        'total': total  # Add total to context
    })

# def decrement_cart(request, cart_id):
#     cart_item = get_object_or_404(Cart, id=cart_id, user=request.user.username)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save(update_fields=['quantity'])
#     else:
#         cart_item.delete()
#     return redirect('view_cart')

def decrement_cart(request, cart_id):
    if not request.user.is_authenticated:
        return redirect('registration')
    
    # Use consistent username filtering
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user.username)
    
    # Add removal option
    if 'remove' in request.GET or cart_item.quantity <= 1:
        cart_item.delete()
        messages.info(request, "Item removed from cart")
    else:
        cart_item.quantity -= 1
        cart_item.save()
    
    return redirect('view_cart')

# def clear_cart(request):
#     Cart.objects.filter(user=request.user.username).delete()
#     messages.success(request, "Your cart has been cleared")
#     return redirect('view_cart')

def clear_cart(request):
    if not request.user.is_authenticated:
        return redirect('registration')
    
    Cart.objects.filter(user=request.user.username).delete()
    messages.success(request, "Your cart has been cleared")
    return redirect('view_cart')

def checkout(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user.username)
    else:
        cart_items = []

    # Calculate grand total
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'home/checkout.html', {
        'cart_total': total
    })


def payment(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user.username)
    else:
        cart_items = []

    # Calculate grand total
    total = sum(item.product.price * item.quantity for item in cart_items)

    settings = { 'store_id': 'test685264cda6bdb', 'store_pass': 'test685264cda6bdb@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = {total}
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = 'http://127.0.0.1:8000/payment/success/'
    post_body['fail_url'] = 'http://127.0.0.1:8000/payment/fail/'
    post_body['cancel_url'] = 'http://127.0.0.1:8000/payment/cancel/'
    post_body['emi_option'] = 0
    post_body['cus_name'] = "test"
    post_body['cus_email'] = "test@test.com"
    post_body['cus_phone'] = "01700000000"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    # print(response)
    return HttpResponseRedirect(response['GatewayPageURL'])


from django.http import HttpResponse

@csrf_exempt
def payment_success(request):
    return HttpResponse("Payment Successful")

@csrf_exempt
def payment_fail(request):
    return HttpResponse("Payment Failed")

@csrf_exempt
def payment_cancel(request):
    return HttpResponse("Payment Cancelled")
