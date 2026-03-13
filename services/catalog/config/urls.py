from django.contrib import admin
from django.urls import path
from apps.products.routes import router as router_products
from ninja_extra import NinjaExtraAPI

app = NinjaExtraAPI()
app.add_router("products/", router_products)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', app.urls)
]
