from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'material', 'price', 'is_new', 'is_bestseller']
    list_filter = ['category', 'material', 'is_new', 'is_bestseller']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_new', 'is_bestseller']
    fields = ['name', 'category', 'material', 'price', 'description', 'characteristics', 
              'image', 'is_new', 'is_bestseller']  