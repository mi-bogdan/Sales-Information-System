from django.db import models


class Contact(models.Model):
    """Контактные данные для новостей"""
    email = models.EmailField(unique=True, verbose_name='Почта')
    data = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        db_table = "Contact"
