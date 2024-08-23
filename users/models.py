from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Model for User"""

    username = None
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        help_text="Укажите почту"
    )
    phone = models.CharField(
        verbose_name="Телефон",
        max_length=35,
        help_text="Укажите телефон", **NULLABLE
    )
    city = models.CharField(
        verbose_name="Город",
        max_length=35,
        help_text="Укажите город", **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите фото профиля",
        **NULLABLE,
    )
    tg_chat_id = models.CharField(
        verbose_name="ID чата в Телеграм",
        max_length=35,
        help_text="Укажите ID чата в Телеграм",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"