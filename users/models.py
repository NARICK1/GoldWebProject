from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField('Полное имя', max_length=150, blank=True)
    
    def __str__(self):
        return self.full_name or self.user.username