from django.db import models
from django.conf import settings
from main.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('confirmed', 'Подтверждён'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='orders', verbose_name='Пользователь'
    )
    full_name = models.CharField('ФИО', max_length=200)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    address = models.TextField('Адрес доставки')
    city = models.CharField('Город', max_length=100)
    postal_code = models.CharField('Почтовый индекс', max_length=20, blank=True)
    comment = models.TextField('Комментарий к заказу', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField('Сумма заказа', max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return f'Заказ #{self.id} — {self.full_name}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items', verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL,
        null=True, verbose_name='Товар'
    )
    product_name = models.CharField('Название товара', max_length=200)
    product_price = models.DecimalField('Цена', max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField('Количество', default=1)

    def total(self):
        return self.product_price * self.quantity

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
