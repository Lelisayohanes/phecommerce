from django.contrib import admin
from .models import Product, ProductImage,Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_type', 'image_url')
    list_filter = ('image_type',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
        search_fields = ('name', 'description')

    

