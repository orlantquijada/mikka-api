from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from src.users.views import UserViewSet

ROUTER = SimpleRouter(trailing_slash=False)
ROUTER.register("users", UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(ROUTER.urls),
    ),
]
