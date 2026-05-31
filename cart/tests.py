from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Product
from .models import CartItem

User = get_user_model()


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123!'
        )
        self.product = Product.objects.create(
            name='Кольцо', category='ring', material='gold', price=50000
        )
        self.cart_item = CartItem.objects.create(
            user=self.user, product=self.product, quantity=2
        )

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.product, self.product)

    def test_total_method(self):
        self.assertEqual(self.cart_item.total(), 100000)

    def test_str(self):
        expected = f'{self.user.email} - {self.product.name} x{self.cart_item.quantity}'
        self.assertEqual(str(self.cart_item), expected)


class CartViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123!'
        )
        self.product = Product.objects.create(
            name='Кольцо', category='ring', material='gold', price=50000
        )

    def test_cart_requires_login(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_cart_view_empty(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Корзина')

    def test_add_to_cart(self):
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_add_to_cart_increases_quantity(self):
        self.client.login(username='test@example.com', password='testpass123!')
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        cart_item = CartItem.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_cart_view_with_items(self):
        self.client.login(username='test@example.com', password='testpass123!')
        CartItem.objects.create(user=self.user, product=self.product, quantity=3)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'КОРЗИНА')

    def test_remove_from_cart(self):
        self.client.login(username='test@example.com', password='testpass123!')
        item = CartItem.objects.create(user=self.user, product=self.product)
        response = self.client.post(reverse('remove_from_cart', args=[item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_remove_from_cart_other_user(self):
        other_user = User.objects.create_user(
            username='other', email='other@example.com', password='pass123!'
        )
        item = CartItem.objects.create(user=other_user, product=self.product)
        self.client.login(username='test@example.com', password='testpass123!')
        response = self.client.post(reverse('remove_from_cart', args=[item.id]))
        self.assertEqual(response.status_code, 404)
