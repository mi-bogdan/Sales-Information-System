from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from django.urls import reverse_lazy


class Category(MPTTModel):
    """Категории"""
    title = models.CharField(verbose_name='Категория', max_length=100)
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    parent = TreeForeignKey(
        'self', verbose_name="Родитель", related_name='children', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "Category"


class Prefix(models.Model):
    """Префикс к товарам"""
    title = models.CharField(verbose_name='Префикс', max_length=50)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Префикс"
        verbose_name_plural = "Префиксы"
        db_table = "Prefix"


class Produkt(models.Model):
    """Товары"""
    DISCOUNT = (
        (0, 'нет скидки'),
        (5, '5%'),
        (8, '8%'),
        (10, '10%'),
        (12, '12%'),
        (15, '15%'),
        (20, '20%'),
    )

    title = models.CharField(verbose_name='Название', max_length=255)
    descriptions = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE)
    img = models.ImageField(verbose_name="Изображение",
                            upload_to='shop/%Y/%m/%d')
    slug = models.SlugField(verbose_name='Слаг', max_length=160, unique=True)
    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name='Цена')
    create_at = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True)
    update_at = models.DateTimeField(
        verbose_name="Дата обновления", auto_now=True)
    published = models.BooleanField(
        verbose_name='Публикация товара', default=True)
    discount = models.PositiveSmallIntegerField(
        verbose_name='Скидка', blank=True, default=0, choices=DISCOUNT)
    sku = models.CharField(verbose_name='Артикул', max_length=15, unique=True)
    prefix = models.ForeignKey(
        Prefix, verbose_name='Префикс', on_delete=models.PROTECT, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.sku = self.sku.upper()
        return super(Produkt, self).save(*args, **kwargs)

    def get_reviews(self):
        return self.reviews_set.filter(perents__isnull=True)

    def get_sale(self):
        """Расчитать стоимость со скидкой"""
        price = int(self.price * (100 - self.discount) / 100)
        return price

    def main_category(self):
        return self.category.parent if self.category.parent else self.category

    def save_money(self):
        return self.price - (int(self.price * (100 - self.discount) / 100))

    def formattedprice(self):
        return "%01.2f" % self.price

    def formattedprice_discount(self):
        return "%01.2f" % self.get_sale()

    def get_absolute_url(self):
        return reverse_lazy('deteil', kwargs={'slug': self.slug})

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        db_table = "Produkt"


class Feature(models.Model):
    """Элементы характеристики"""

    title = models.CharField(
        verbose_name="Наименование характеристики", max_length=40)
    value = models.CharField(verbose_name="Значение", max_length=30)

    class Meta:
        abstract = True


class CategoryFeature(Feature):
    "Характеристики категории"

    categories = models.ManyToManyField(Category, verbose_name="Категория", related_name="feature_category",
                                        blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Характиерстика категорий"
        verbose_name_plural = "Характеристики категорий"
        db_table = "CategoryFeature"


class ProductFeature(Feature):
    "Характеристики товара"

    products = models.ManyToManyField(Produkt, verbose_name="Продукт(ы)", related_name="feature_prod",
                                      blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Характиерстика продукта"
        verbose_name_plural = "Характеристики продуктов"
        db_table = "ProductFeature"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField(verbose_name="Имя", max_length=100)
    text = models.TextField(verbose_name="Отписание", max_length=5000)
    perents = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    produkt = models.ForeignKey(
        Produkt, verbose_name="Продукт", on_delete=models.CASCADE)
    create_at = models.DateTimeField(
        verbose_name="Дата отзыва", auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}-{self.produkt}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        db_table = "Reviews"


class ImageProduct(models.Model):
    """Изображение к продуктам"""

    img = models.ImageField(verbose_name="Изображение продукта",
                            upload_to='produkt_images/%Y/%m/%d')
    produkt = models.ForeignKey(
        Produkt, verbose_name="Продукт", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.produkt}'

    class Meta:
        verbose_name = "Изображение к продукту"
        verbose_name_plural = "Изображение к продуктам"
        db_table = "ImageProduct"
