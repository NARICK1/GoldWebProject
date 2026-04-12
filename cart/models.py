from django.db import models
from django.contrib.auth import get_user_model
from main.models import Product

User = get_user_model()

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f'{self.user.email} - {self.product.name} x{self.quantity}'