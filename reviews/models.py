from django.db import models

class Review(models.Model):
    RATING_CHOICES = [
        (1, '★ 1'),
        (2, '★★ 2'),
        (3, '★★★ 3'),
        (4, '★★★★ 4'),
        (5, '★★★★★ 5'),
    ]
    
    PRODUCT_CHOICES = [
        ('ring', '💍 Кольцо'),
        ('earrings', '✨ Серьги'),
        ('necklace', '📿 Подвеска'),
        ('bracelet', '🔗 Браслет'),
    ]
    
    MATERIAL_CHOICES = [  
        ('gold', '🟡 Золото'),
        ('silver', '⚪ Серебро'),
        ('rose', '🌸 Розовое золото'),
        ('platinum', '🤍 Платина'),
        ('black', '⚫ Чёрное золото'),
        ('meteorite', '☄️ Метеорит (Новинка)'),  
    ]
    
    product_type = models.CharField('Тип изделия', max_length=20, choices=PRODUCT_CHOICES, default='ring')
    material = models.CharField('Материал', max_length=20, choices=MATERIAL_CHOICES, default='gold')  # 👈 НОВОЕ ПОЛЕ
    product_name = models.CharField('Название изделия', max_length=200, blank=True)
    author_name = models.CharField('Имя автора', max_length=100)
    author_email = models.EmailField('Email', blank=True)
    topic = models.CharField('Тема отзыва', max_length=200)
    text = models.TextField('Текст отзыва')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES, default=5)
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    is_published = models.BooleanField('Опубликован', default=True)
    
    def __str__(self):
        return f'{self.author_name} - {self.topic}'
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']