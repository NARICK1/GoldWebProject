from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Product
from .models import Favorite

User = get_user_model()


class FavoriteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123!'
        )
        self.product = Product.objects.create(
            name='Кольцо', category='ring', material='gold', price=50000
        )
        self.favorite = Favorite.objects.create(user=self.user, product=self.product)

    def test_favorite_creation(self):
        self.assertEqual(self.favorite.user, self.user)
        self.assertEqual(self.favorite.product, self.product)

    def test_unique_together(self):
        with self.assertRaises(Exception):
            Favorite.objects.create(user=self.user, product=self.product)

    def test_str(self):
        expected = f'{self.user.email} - {self.product.name}'
        self.assertEqual(str(self.favorite), expected)


class FavoriteViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123!'
        )
        self.product = Product.objects.create(
            name='Кольцо', category='ring', material='gold', price=50000
        )

    def test_favorites_requires_login(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_favorites_view_empty(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ИЗБРАННОЕ')

    def test_add_to_favorites(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.get(reverse('add_to_favorites', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favorite.objects.filter(user=self.user, product=self.product).exists())

    def test_add_to_favorites_twice(self):
        self.client.login(username='test@example.com', password='testpass123!')
        self.client.get(reverse('add_to_favorites', args=[self.product.id]))
        self.client.get(reverse('add_to_favorites', args=[self.product.id]))
        self.assertEqual(Favorite.objects.filter(user=self.user).count(), 1)

    def test_remove_from_favorites(self):
        self.client.login(username='test@example.com', password='testpass123!')
        Favorite.objects.create(user=self.user, product=self.product)
        response = self.client.get(reverse('remove_from_favorites', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Favorite.objects.filter(user=self.user, product=self.product).exists())

    def test_favorites_view_with_items(self):
        self.client.login(username='test@example.com', password='testpass123!')
        Favorite.objects.create(user=self.user, product=self.product)
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Кольцо')
