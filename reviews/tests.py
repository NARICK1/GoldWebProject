from django.test import TestCase, Client
from django.urls import reverse
from main.models import Product
from .models import Review


class ReviewModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Кольцо', category='ring', material='gold', price=50000
        )
        self.review = Review.objects.create(
            product=self.product,
            author_name='Иван',
            author_email='ivan@example.com',
            product_type='ring',
            material='gold',
            topic='Отличное кольцо',
            text='Очень красивое кольцо, спасибо!',
            rating=5,
            is_published=True,
        )

    def test_review_creation(self):
        self.assertEqual(self.review.author_name, 'Иван')
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.rating, 5)

    def test_review_str(self):
        expected = 'Иван - Отличное кольцо'
        self.assertEqual(str(self.review), expected)

    def test_unpublished_review(self):
        review = Review.objects.create(
            author_name='Петр',
            product_type='ring',
            material='gold',
            topic='Тест',
            text='Тест',
            rating=3,
            is_published=False,
        )
        self.assertFalse(review.is_published)

    def test_review_product_nullable(self):
        review = Review.objects.create(
            author_name='Тест',
            product_type='ring',
            material='gold',
            topic='Без товара',
            text='Тест',
            rating=4,
            is_published=True,
        )
        self.assertIsNone(review.product)


class ReviewViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Кольцо', category='ring', material='gold', price=50000
        )
        self.review = Review.objects.create(
            product=self.product,
            author_name='Иван',
            author_email='ivan@example.com',
            product_type='ring',
            material='gold',
            topic='Отличное кольцо',
            text='Очень красивое кольцо, спасибо!',
            rating=5,
            is_published=True,
        )

    def test_reviews_list_page(self):
        response = self.client.get(reverse('reviews_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Иван')

    def test_add_review_success(self):
        response = self.client.post(reverse('add_review'), {
            'author_name': 'Петр',
            'author_email': 'petr@example.com',
            'product_type': 'ring',
            'material': 'gold',
            'product_name': 'Кольцо',
            'topic': 'Хороший товар',
            'text': 'Мне понравилось!',
            'rating': 4,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 2)

    def test_add_review_invalid_email(self):
        response = self.client.post(reverse('add_review'), {
            'author_name': 'Петр',
            'author_email': 'invalid-email',
            'product_type': 'ring',
            'material': 'gold',
            'topic': 'Тест',
            'text': 'Тест',
            'rating': 3,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)

    def test_add_review_cyrillic_email(self):
        response = self.client.post(reverse('add_review'), {
            'author_name': 'Петр',
            'author_email': 'петр@example.com',
            'product_type': 'ring',
            'material': 'gold',
            'topic': 'Тест',
            'text': 'Тест',
            'rating': 3,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)

    def test_average_rating_calculation(self):
        Review.objects.create(
            author_name='Анна',
            author_email='anna@example.com',
            product_type='ring',
            material='gold',
            topic='Хорошо',
            text='Неплохо',
            rating=3,
            is_published=True,
        )
        response = self.client.get(reverse('reviews_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Анна')

    def test_unpublished_reviews_not_shown(self):
        Review.objects.create(
            author_name='Невидимый',
            product_type='ring',
            material='gold',
            topic='Не опубликован',
            text='Не виден',
            rating=1,
            is_published=False,
        )
        response = self.client.get(reverse('reviews_list'))
        self.assertNotContains(response, 'Невидимый')
