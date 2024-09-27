from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users_app.models import User


class Brand(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=500)

class Category(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=500)

class Product(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveBigIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)