# Generated by Django 5.1.1 on 2024-10-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_product_discount_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_desc',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]