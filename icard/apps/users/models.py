from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from icard.apps.users.utils.user_manage import UserManager
from django.db import models

from icard.utils.models import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    identification_number = models.CharField(
        unique=True,
        max_length=12,
        null=True,
        blank=True
    )
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15)
    ip_address = models.JSONField(default=dict, null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        app_label = "users"

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "phone_number"]

    @property
    def user_full_name(self):
        formatted_user_name = list()
        if self.first_name:
            formatted_user_name.append(self.first_name)
        if self.last_name:
            formatted_user_name.append(self.last_name)
        return " ".join(formatted_user_name)

    @property
    def is_admin(self):
        return self.is_staff and self.groups.filter(name="admin").exists()

    def __str__(self):
        return self.first_name if self.first_name else self.phone_number
