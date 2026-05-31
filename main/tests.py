from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Тестовое кольцо',
            category='ring',
            material='gold',
            price=50000,
            description='Описание',
            characteristics='Характеристики',
            is_new=True,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Тестовое кольцо')
        self.assertEqual(self.product.category, 'ring')
        self.assertEqual(self.product.material, 'gold')
        self.assertEqual(self.product.price, 50000)
        self.assertTrue(self.product.is_new)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Тестовое кольцо')

    def test_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), f'/catalog/{self.product.id}/')

    def test_default_values(self):
        product = Product.objects.create(name='Минимальное')
        self.assertEqual(product.price, 0)
        self.assertFalse(product.is_bestseller)


class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Кольцо',
            category='ring',
            material='gold',
            price=30000,
        )

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/blackhole.html')

    def test_home_page_light_theme(self):
        response = self.client.get('/', cookies={'theme': 'light'})
        self.assertEqual(response.status_code, 200)

    def test_catalog_page(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Кольцо')

    def test_catalog_filter_by_category(self):
        response = self.client.get(reverse('catalog') + '?category=ring')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Кольцо')

    def test_catalog_filter_no_results(self):
        response = self.client.get(reverse('catalog') + '?category=bracelet')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Товары пока не добавлены')

    def test_product_detail(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Кольцо')

    def test_product_detail_404(self):
        response = self.client.get(reverse('product_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)


class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_page_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'DifferentPass!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='test@example.com').exists())

    def test_register_duplicate_email(self):
        User.objects.create_user(username='existing', email='test@example.com', password='pass123!')
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 200)

    def test_register_invalid_username(self):
        response = self.client.post(reverse('register'), {
            'username': '@@@invalid@@@',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 200)


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='TestPass123!'
        )

    def test_login_page_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_fail_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)


class URLTests(TestCase):
    def test_all_urls_reverse(self):
        urls = ['home', 'catalog', 'about', 'contact', 'login', 'register']
        for name in urls:
            with self.subTest(url=name):
                self.assertTrue(reverse(name))
