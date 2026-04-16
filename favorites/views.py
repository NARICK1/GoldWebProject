from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Product
from .models import Favorite

@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'favorites/favorites.html', {'favorites': favorites})

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f'Товар "{product.name}" добавлен в избранное')
    else:
        messages.info(request, f'Товар "{product.name}" уже в избранном')
    
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))

@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'Товар "{product.name}" удалён из избранного')
    return redirect(request.META.get('HTTP_REFERER', 'favorites'))