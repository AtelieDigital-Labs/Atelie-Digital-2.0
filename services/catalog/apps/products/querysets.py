from django.db import models
from django.db.models import Prefetch
from django.apps import apps

class ProductQuerySet(models.QuerySet):
    def with_variant_main(self):
        Variant = apps.get_model('products', 'Variant')
        return self.prefetch_related(Prefetch(
        'variants',
        queryset=Variant.objects.filter(is_main=True)[:1],
        to_attr="variant"
    ))
    