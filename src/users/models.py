from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(
    AbstractUser,
    PermissionsMixin,
):
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f"{self.id} / {self.get_full_name()}"
