from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Ensure unique category names
    description = models.TextField(blank=True)  # Optional description for the category

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)  # Keep categories in DB even if products are deleted.

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    IMAGE_TYPES = (
        ('main', 'Main Image'),
        ('front', 'Front Image'),
        ('back', 'Back Image'),
        ('left', 'Left Image'),
        ('right', 'Right Image'),
        ('modelOne', 'Model Image One'),
        ('modelTwo', 'Model Image Two'),
    )
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPES)
    image_url = models.ImageField(upload_to='product_images/')  # Store images in the specified directory

    def __str__(self):
        return f"{self.product.name} - {self.image_type}"
