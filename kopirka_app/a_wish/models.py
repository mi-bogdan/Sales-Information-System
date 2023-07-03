from django.db import models
from django.contrib.auth.models import User
from shop.models import Produkt


class A_Wish(models.Model):
    """Список желаний"""
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(
        Produkt, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self) -> str:
        return f'{self.user}--{self.product}'

    class Meta:
        verbose_name = "Желание"
        verbose_name_plural = "Желания"
        db_table = "Wish"
