# Generated by Django 5.1.5 on 2025-02-07 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_product_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='admin',
        ),
    ]
