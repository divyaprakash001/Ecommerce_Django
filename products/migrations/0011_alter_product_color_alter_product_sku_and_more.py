# Generated by Django 5.1.1 on 2024-10-13 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_tags_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.CharField(max_length=50),
        ),
    ]
