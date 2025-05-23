from django.contrib import admin
from . models import Category, Product, Size, Brand, Review

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'size', 'brand', 'discount', 'condition', 'in_stock', 'quantity'] 

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'comment', 'email'] 



admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Review, ReviewAdmin)
