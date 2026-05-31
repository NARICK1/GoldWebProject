from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Product
from cart.models import CartItem
from .models import Order, OrderItem

User = get_user_model()


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123!'
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Иван Иванов',
            phone='+7 (937) 476-88-11',
            email='test@example.com',
            address='ул. Ленина, д. 1',
            city='Уфа',
            total_price=100000,
        )

    def test_order_creation(self):
        self.assertEqual(self.order.full_name, 'Иван Иванов')
        self.assertEqual(self.order.total_price, 100000)
        self.assertEqual(self.order.status, 'pending')

    def test_order_str(self):
        expected = f'Заказ #{self.order.id} — Иван Иванов'
        self.assertEqual(str(self.order), expected)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123!'
        )
        self.product = Product.objects.create(
            name='Кольцо', category='ring', material='gold', price=50000
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Иван Иванов',
            phone='+7 (937) 476-88-11',
            email='test@example.com',
            address='ул. Ленина, д. 1',
            city='Уфа',
            total_price=100000,
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            product_price=self.product.price,
            quantity=2,
        )

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.product_name, 'Кольцо')
        self.assertEqual(self.order_item.quantity, 2)

    def test_total_method(self):
        self.assertEqual(self.order_item.total(), 100000)

    def test_str(self):
        expected = f'{self.order_item.product_name} x{self.order_item.quantity}'
        self.assertEqual(str(self.order_item), expected)

    def test_order_item_deletes_with_order(self):
        item_id = self.order_item.id
        self.order.delete()
        self.assertFalse(OrderItem.objects.filter(id=item_id).exists())


class OrderViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123!'
        )
        self.product = Product.objects.create(
            name='Кольцо', category='ring', material='gold', price=50000
        )
        self.client.login(username='test@example.com', password='testpass123!')

    def test_checkout_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_checkout_empty_cart_redirects(self):
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('cart'))

    def test_checkout_page_with_items(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ОФОРМЛЕНИЕ ЗАКАЗА')

    def test_checkout_success(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        response = self.client.post(reverse('checkout'), {
            'full_name': 'Иван Иванов',
            'phone': '+7 (937) 476-88-11',
            'email': 'test@example.com',
            'address': 'ул. Ленина, д. 1',
            'city': 'Уфа',
            'postal_code': '450000',
            'comment': 'Позвонить перед доставкой',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 0)

        order = Order.objects.first()
        self.assertEqual(order.total_price, 100000)
        self.assertEqual(order.full_name, 'Иван Иванов')

    def test_checkout_missing_fields(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        response = self.client.post(reverse('checkout'), {
            'full_name': '',
            'phone': '',
            'email': '',
            'address': '',
            'city': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_success_page(self):
        order = Order.objects.create(
            user=self.user,
            full_name='Иван Иванов',
            phone='+7 (937) 476-88-11',
            email='test@example.com',
            address='ул. Ленина, д. 1',
            city='Уфа',
            total_price=100000,
        )
        response = self.client.get(reverse('order_success', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Спасибо за заказ')

    def test_order_success_wrong_user(self):
        other_user = User.objects.create_user(
            username='other', email='other@example.com', password='pass123!'
        )
        order = Order.objects.create(
            user=other_user,
            full_name='Другой',
            phone='+7 (999) 999-99-99',
            email='other@example.com',
            address='ул. Другая',
            city='Москва',
            total_price=100000,
        )
        response = self.client.get(reverse('order_success', args=[order.id]))
        self.assertEqual(response.status_code, 404)

    def test_order_history(self):
        Order.objects.create(
            user=self.user,
            full_name='Иван Иванов',
            phone='+7 (937) 476-88-11',
            email='test@example.com',
            address='ул. Ленина, д. 1',
            city='Уфа',
            total_price=50000,
        )
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Заказ #')

    def test_order_history_empty(self):
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'нет заказов')
