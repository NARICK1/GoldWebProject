import re
import socket
from django.core.exceptions import ValidationError

ALLOWED_DOMAIN_ZONES = [
    'com', 'ru', 'net', 'org', 'ua', 'by', 'kz', 'uz',
    'info', 'biz', 'me', 'site', 'online', 'shop', 'store',
    'mail', 'in', 'us', 'eu', 'de', 'fr', 'uk', 'pl', 'cz',
    'tr', 'il', 'jp', 'cn', 'br', 'au', 'ca', 'io', 'app',
    'world', 'space', 'club', 'xyz', 'top', 'work', 'live',
]


def validate_email(email):
    if not email:
        return True, ''

    if re.search(r'[а-яА-ЯёЁ]', email):
        return False, 'Email не должен содержать русские буквы!'

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False, 'Неверный формат email! Пример: name@mail.ru'

    zone = email.split('.')[-1].lower()
    if zone not in ALLOWED_DOMAIN_ZONES:
        return False, f"Доменная зона '.{zone}' не поддерживается"

    return True, ''


def validate_email_strict(email):
    is_valid, msg = validate_email(email)
    if not is_valid:
        raise ValidationError(msg)
    domain = email.split('@')[1]
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        raise ValidationError(f'Домен "{domain}" не существует! Введите реальный email.')
    return email
