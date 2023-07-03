# Generated by Django 4.1.7 on 2023-05-19 16:50

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_categoryspecifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryspecifications',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childrens', to='shop.categoryspecifications', verbose_name='Родитель'),
        ),
    ]