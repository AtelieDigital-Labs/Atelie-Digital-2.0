from django.contrib import admin
from django.urls import path
from apps.users.routes import router as router_users
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

api = NinjaExtraAPI(title="Ateliê Digital", description="Endpoints de accounts")

api.register_controllers(NinjaJWTDefaultController)

api.add_router("users/", router_users)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
