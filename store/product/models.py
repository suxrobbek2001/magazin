import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models import PROTECT

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    image = models.ImageField(upload_to=os.path.join('uploads', 'images'))
    category = models.ForeignKey(Category, on_delete=PROTECT)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1, related_name='carts')

    def __str__(self):
        return  f"{self.product.name} - {"user->"} {self.user.username}"

    # @classmethod
    # def calculate_total(cls, user):
    #     """Calculate the total sum of products in the cart for a specific user."""
    #     total = sum(cart.product.price for cart in cls.objects.filter(user=user))
    #     return total



