from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'product', 'product_type', 'material', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating', 'product_type', 'material')
    search_fields = ('author_name', 'author_email', 'topic', 'text')
    list_editable = ('is_published',)