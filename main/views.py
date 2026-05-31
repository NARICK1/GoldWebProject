from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .models import Product
from users.forms import CustomUserCreationForm

def home(request):
    theme = request.COOKIES.get('theme', 'dark')
    if theme == 'light':
        return render(request, 'main/home_light.html')
    else:
        return render(request, 'main/blackhole.html')

def catalog(request):
    products = Product.objects.all().order_by('-created_at')
    
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    
    material = request.GET.get('material')
    if material:
        products = products.filter(material=material)
    
    context = {
        'products': products,
        'title': 'Каталог'
    }
    return render(request, 'main/catalog.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
        'title': product.name
    }
    return render(request, 'main/product_detail.html', context)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})