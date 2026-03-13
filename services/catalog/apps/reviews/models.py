from django.db import models
from apps.products.models import Product

class ProductReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.IntegerField()
    rating = models.PositiveSmallIntegerField() 
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating} estrelas"
