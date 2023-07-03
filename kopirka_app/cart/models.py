from django.db import models
from django.contrib.auth.models import User
from shop.models import Produkt


class Cart(models.Model):
    """Корзина"""
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    session_id = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Ключ_сессии')
    total_price = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0, verbose_name='Сумма_корзины', null=True)

    def __str__(self) -> str:
        return f'{self.user}--{self.session_id}'

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "корзины"
        db_table = "Cart"


class CartItem(models.Model):
    """Элементы корзины"""
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(
        Produkt, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(
        default=0, verbose_name='Кол-во_товара(шт)')
    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name='Цена_по_количеству')

    def __str__(self) -> str:
        return f'{self.cart}--{self.product}'

    class Meta:
        verbose_name = "ЭлементКорзины"
        verbose_name_plural = "ЭлементыКорзины"
        db_table = "CartItem"
