# Generated by Django 5.1.1 on 2024-10-10 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['category_name'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='category_pic',
            field=models.ImageField(null=True, upload_to='products/categories'),
        ),
        migrations.AlterModelTable(
            name='category',
            table='category',
        ),
    ]
