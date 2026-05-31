from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg, Count
import re
from .models import Review
from main.models import Product  # 👈 ИСПРАВЛЕНО

# Список разрешённых доменных зон
ALLOWED_DOMAINS = [
    'com', 'ru', 'net', 'org', 'ua', 'by', 'kz', 'uz', 
    'info', 'biz', 'me', 'site', 'online', 'shop', 'store',
    'mail', 'in', 'us', 'eu', 'de', 'fr', 'uk', 'pl', 'cz',
    'tr', 'il', 'jp', 'cn', 'br', 'au', 'ca', 'io', 'app',
    'world', 'space', 'club', 'xyz', 'top', 'work', 'live'
]

def validate_email(email):
    if not email:
        return True, ""
    if re.search(r'[а-яА-ЯёЁ]', email):
        return False, "Email не должен содержать русские буквы!"
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False, "Неверный формат email! Пример: name@mail.ru"
    domain = email.split('.')[-1].lower()
    if domain not in ALLOWED_DOMAINS:
        return False, f"Доменная зона '.{domain}' не поддерживается"
    return True, ""

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
        
        try:
            review = Review.objects.create(
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