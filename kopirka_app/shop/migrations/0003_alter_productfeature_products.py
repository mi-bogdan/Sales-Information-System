# Generated by Django 4.1.7 on 2023-04-12 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_produkt_prefix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeature',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='feature_prod', to='shop.produkt', verbose_name='Продукт(ы)'),
        ),
    ]
