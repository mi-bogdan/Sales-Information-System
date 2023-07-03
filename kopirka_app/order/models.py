from django.db import models
from django.contrib.auth.models import User
from shop.models import Produkt


class DeliveryMethod(models.Model):
    """Способ доставки"""
    title = models.CharField(verbose_name='Название', max_length=100)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Способ доставки"
        verbose_name_plural = "Способы доставки"
        db_table = "DeliveryMethod"


class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = (
        ('Нов', 'Новый заказ'),
        ('Обр', 'В обработке'),
        ('При', 'Принят'),
        ('Дос', 'Доставляется'),
        ('Вып', 'Выполнен'),
        ('Отм', 'Отменено'),
        ('Воз', 'Возврат'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь', blank=True, null=True)
    session_id = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Ключ_сессии')
    status = models.CharField(verbose_name='Статус_заказа',
                              choices=STATUS_CHOICES, default='Нов', max_length=3)
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта')
    phone = models.CharField(verbose_name='Телефон', max_length=12)
    address = models.CharField(max_length=150, verbose_name='Адрес')
    city = models.CharField(max_length=40, verbose_name='Город')
    note_order = models.TextField(
        verbose_name='Примечание к заказу', blank=True, null=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name='Сумма_корзины', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Дата обновления')
    delivery_date = models.DateField(
        verbose_name='Дата доставки', blank=True, null=True)
    delivery_method = models.ForeignKey(
        DeliveryMethod, verbose_name='Способ доставки', on_delete=models.PROTECT)
    payment = models.BooleanField(verbose_name='Оплата заказа', default=False)

    def __str__(self) -> str:
        return f'{self.first_name}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        db_table = "Order"


class OrderItem(models.Model):
    """Элементы заказа"""
    order = models.ForeignKey(
        Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='ord')
    product = models.ForeignKey(
        Produkt, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(
        default=0, verbose_name='Кол-во_товара(шт)')
    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name='Цена_по_количеству')

    def __str__(self) -> str:
        return f'{self.order}--{self.product}'

    class Meta:
        verbose_name = "ЭлементЗаказа"
        verbose_name_plural = "ЭлементыЗаказа"
        db_table = "OrderItem"
