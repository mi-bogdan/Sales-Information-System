# Generated by Django 4.1.7 on 2023-05-19 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_categoryspecifications_parent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CategorySpecifications',
        ),
    ]
