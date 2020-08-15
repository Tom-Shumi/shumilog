from django.contrib.auth.models import AbstractUser


class ShumilogUser(AbstractUser):
    class Meta:
        verbose_name_plural = 'ShumilogUser'

