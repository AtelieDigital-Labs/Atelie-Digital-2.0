from django.db import models
from .querysets import ProductQuerySet

class ProductManager(models.Manager, ProductQuerySet):
    def with_variant_main(self):
        return self.get_queryset().with_variant_main()