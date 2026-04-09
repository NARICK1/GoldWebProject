from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        help_text='Можно использовать русские буквы, английские буквы, цифры и пробел',
        max_length=150
    )
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Разрешаем: русские буквы, английские буквы, цифры, пробел, точку, дефис, подчёркивание
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9\s\.\-_]+$', username):
            raise forms.ValidationError('Имя пользователя может содержать только буквы (русские/английские), цифры, пробел, точку, дефис и подчёркивание')
        
        # Проверка на уникальность
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
        
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2