from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Product.models import Product
# Create your views here.

@login_required(login_url='registration')
def home(request):
    # Get products marked as featured (or any other condition you want)
    featured_products = Product.objects.filter(featured=True, in_stock=True, image__isnull=False)[:6]
    return render(request, 'home/home.html', {'featured_products': featured_products})
