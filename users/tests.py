from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from main.validators import validate_email, validate_email_strict

User = get_user_model()


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123!'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')

    def test_email_unique(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='another', email='test@example.com', password='pass123!'
            )

    def test_username_not_unique(self):
        User.objects.create_user(
            username='testuser', email='other@example.com', password='pass123!'
        )
        self.assertEqual(User.objects.filter(username='testuser').count(), 2)

    def test_str(self):
        self.assertEqual(str(self.user), 'test@example.com')

    def test_login_by_email(self):
        user = User.objects.get(email='test@example.com')
        self.assertTrue(user.check_password('testpass123!'))

    def test_email_as_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')


class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form = CustomUserCreationForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass1!',
            'password2': 'StrongPass1!',
        })
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form = CustomUserCreationForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass1!',
            'password2': 'DifferentPass!',
        })
        self.assertFalse(form.is_valid())

    def test_invalid_username_symbols(self):
        form = CustomUserCreationForm(data={
            'username': '@@@invalid@@@',
            'email': 'new@example.com',
            'password1': 'StrongPass1!',
            'password2': 'StrongPass1!',
        })
        self.assertFalse(form.is_valid())

    def test_email_with_cyrillic(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'test@пример.com',
            'password1': 'StrongPass1!',
            'password2': 'StrongPass1!',
        })
        self.assertFalse(form.is_valid())

    def test_email_invalid_format(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': 'notanemail',
            'password1': 'StrongPass1!',
            'password2': 'StrongPass1!',
        })
        self.assertFalse(form.is_valid())

    def test_empty_email(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'email': '',
            'password1': 'StrongPass1!',
            'password2': 'StrongPass1!',
        })
        self.assertFalse(form.is_valid())


class CustomAuthenticationFormTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123!'
        )

    def test_valid_login(self):
        form = CustomAuthenticationForm(data={
            'username': 'test@example.com',
            'password': 'testpass123!',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_login_wrong_email(self):
        form = CustomAuthenticationForm(data={
            'username': 'wrong@example.com',
            'password': 'testpass123!',
        })
        self.assertFalse(form.is_valid())

    def test_invalid_login_wrong_password(self):
        form = CustomAuthenticationForm(data={
            'username': 'test@example.com',
            'password': 'wrongpass',
        })
        self.assertFalse(form.is_valid())


class EmailValidatorTest(TestCase):
    def test_valid_email(self):
        valid, msg = validate_email('test@example.com')
        self.assertTrue(valid)

    def test_empty_email(self):
        valid, msg = validate_email('')
        self.assertTrue(valid)

    def test_cyrillic_email(self):
        valid, msg = validate_email('test@пример.com')
        self.assertFalse(valid)

    def test_invalid_format(self):
        valid, msg = validate_email('notanemail')
        self.assertFalse(valid)

    def test_unsupported_domain(self):
        valid, msg = validate_email('test@example.test')
        self.assertFalse(valid)
