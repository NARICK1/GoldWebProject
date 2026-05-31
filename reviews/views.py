from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Review
from main.models import Product
from main.validators import validate_email


def reviews_list(request):
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')
    avg_rating = Review.objects.filter(is_published=True).aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = Review.objects.filter(is_published=True).count()

    rating_distribution = {}
    for i in range(5, 0, -1):
        count = Review.objects.filter(is_published=True, rating=i).count()
        rating_distribution[i] = count

    context = {
        'reviews': reviews,
        'average_rating': avg_rating,
        'total_reviews': total_reviews,
        'rating_distribution': rating_distribution,
    }
    return render(request, 'reviews/reviews_list.html', context)


def add_review(request):
    if request.method == 'POST':
        email = request.POST.get('author_email', '').strip()

        is_valid, error_message = validate_email(email)
        if not is_valid:
            messages.error(request, error_message)
            return redirect('reviews_list')

        product_id = request.POST.get('product_id')
        product = None
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                pass

        try:
            review = Review.objects.create(
                product=product,
                author_name=request.POST.get('author_name'),
                author_email=email,
                product_type=request.POST.get('product_type'),
                product_name=request.POST.get('product_name', ''),
                material=request.POST.get('material'),
                topic=request.POST.get('topic'),
                text=request.POST.get('text'),
                rating=int(request.POST.get('rating')),
                is_published=True
            )
            messages.success(request, 'Спасибо! Ваш отзыв добавлен.')
        except Exception as e:
            messages.error(request, f'Ошибка при сохранении: {e}')

        return redirect('reviews_list')

    return redirect('reviews_list')