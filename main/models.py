from django.db import models
from django.urls import reverse

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('ring', 'Кольцо'),
        ('earrings', 'Серьги'),
        ('necklace', 'Подвеска'),
        ('bracelet', 'Браслет'),
    ]
    
    MATERIAL_CHOICES = [
        ('gold', 'Золото'),
        ('silver', 'Серебро'),
        ('rose', 'Розовое золото'),
        ('platinum', 'Платина'),
        ('black', 'Чёрное золото'),
        ('meteorite', 'Метеорит'),
    ]
    
    name = models.CharField('Название', max_length=200)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES, default='ring')
    material = models.CharField('Материал', max_length=20, choices=MATERIAL_CHOICES, default='gold')
    price = models.DecimalField('Цена (₽)', max_digits=10, decimal_places=0, default=0)
    description = models.TextField('Описание', blank=True)
    characteristics = models.TextField('Характеристики', blank=True)
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    is_new = models.BooleanField('Новинка', default=False)
    is_bestseller = models.BooleanField('Хит продаж', default=False)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']