import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from main.validators import validate_email_strict

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        help_text='Можно использовать русские буквы, английские буквы, цифры и пробел',
        max_length=150
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        help_text='Введите действующий email'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9\s\.\-_]+$', username):
            raise forms.ValidationError('Имя пользователя может содержать только буквы (русские/английские), цифры, пробел, точку, дефис и подчёркивание')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = validate_email_strict(email)
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2