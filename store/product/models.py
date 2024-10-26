import os

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

    def __str__(self):
        return self.product



