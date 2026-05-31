from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import CartItem
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.info(request, 'Ваша корзина пуста')
        return redirect('cart')

    total_price = sum(item.total() for item in cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        comment = request.POST.get('comment', '').strip()

        errors = []
        if not full_name:
            errors.append('Укажите ФИО')
        if not phone:
            errors.append('Укажите телефон')
        if not email:
            errors.append('Укажите email')
        if not address:
            errors.append('Укажите адрес доставки')
        if not city:
            errors.append('Укажите город')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'orders/checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
            })

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            email=email,
            address=address,
            city=city,
            postal_code=postal_code,
            comment=comment,
            total_price=total_price,
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_price=cart_item.product.price,
                quantity=cart_item.quantity,
            )

        cart_items.delete()
        messages.success(request, f'Заказ #{order.id} оформлен! Мы свяжемся с вами.')
        return redirect('order_success', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
