# Generated by Django 5.1.1 on 2024-10-16 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_product_stock_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='width',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]