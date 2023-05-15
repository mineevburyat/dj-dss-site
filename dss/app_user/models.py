from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(
        verbose_name='аватар',
        upload_to='users',
        null=True,
        blank=True)
    is_verified_email = models.BooleanField(
        verbose_name='верефикация email',
        default=False)


class VerifideUser(models.Model):
    code = models.UUIDField(
        verbose_name='uuid',
        unique=True)
    user = models.ForeignKey(User,
                             verbose_name='пользователь',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='время создания')
    expiration = models.DateTimeField(verbose_name='действует до')

    def __str__(self):
        return f"{self.user.email} - {self.code}"
