from django.db import models


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    user = models.IntegerField(null=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=False, null=True)
    phone_number = models.CharField(unique=True, max_length=15)
    date_creation = models.DateTimeField(auto_now_add=True)
    cnpj = models.CharField(unique=True, max_length=14, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=255)
    image = models.ImageField(upload_to='store/image')
    banner = models.ImageField(upload_to='store/banner')

    def __str__(self):
        return f'{self.name} (ID: {self.store_id})'

    class Meta:
        db_table = 'stores'
