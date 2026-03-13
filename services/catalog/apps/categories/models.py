from django.db import models
from apps.products.models import Product
from apps.stores.models import Store

class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_categories', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} -> {self.category.name}'

    class Meta:
        unique_together = (('category', 'product'),)

class StoreCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='product_categories', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store.name} -> {self.category.name}'

    class Meta:
        unique_together = (('category', 'store'),)