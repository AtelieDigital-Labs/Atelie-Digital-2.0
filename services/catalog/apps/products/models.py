from django.db import models
from apps.stores.models import Store
from .managers import ProductManager
from .querysets import ProductQuerySet

class Product(models.Model):
    store = models.ForeignKey(Store, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="produtos")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} (ID: {self.pk})"


class Favorite(models.Model):
    user = models.IntegerField()
    product = models.ForeignKey(
        Product, related_name="favorites", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.product.name} - Favoritado por {self.user}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="u_user_product")
        ]


class VariantType(models.TextChoices):
    STOCK = "STOCK", "Estoque"
    DEMAND = "DEMAND", "Demanda"


class Variant(models.Model):
    product = models.ForeignKey(
        Product, related_name="variants", on_delete=models.CASCADE
    )
    sku = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(
        max_length=7, choices=VariantType, default=VariantType.STOCK
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(blank=True, null=True)
    production_days = models.IntegerField(blank=True, null=True)
    is_customizable = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.type == "STOCK" and self.stock is None:
            raise ValidationError("Produtos de estoque precisam de stock.")

        if self.type == "DEMAND" and self.production_days is None:
            raise ValidationError("Produtos sob demanda precisam de production_days.")

    def __str__(self):
        return f"{self.product.name} - SKU: {self.sku}"

    class Meta:
        unique_together = [["sku", "product"]]


class VariantImage(models.Model):
    product_variant = models.ForeignKey(
        Variant, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/variants")

    def __str__(self):
        return f"Imagem da variante {self.product_variant.sku}"


class Attribute(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class VariantAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(
        Variant, related_name="variant_attributes", on_delete=models.CASCADE
    )
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product_variant.sku} - {self.attribute.name}: {self.value}"

    class Meta:
        unique_together = (("attribute", "product_variant"),)

    # def save(self, *args, **kwargs):
    #     qs = VariantAttribute.objects.filter(
    #         product_variant=self.product_variant, attribute=self.attribute
    #     )

    #     if self.pk:
    #         qs = qs.exclude(pk=self.pk)

    #     if qs.exists():
    #         qs.delete()

    #     super().save(*args, **kwargs)
