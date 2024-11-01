# Generated by Django 5.1.1 on 2024-10-13 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_category_category_slug'),
        ('seller', '0007_seller_seller_linkedin_url_seller_seller_youtube_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=30, unique=True)),
                ('tag_desc', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Tags',
                'verbose_name_plural': 'Tags',
                'db_table': 'tags',
                'ordering': ['tag_name'],
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='seller.seller'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=50, unique=True)),
                ('product_name', models.CharField(max_length=100, unique=True)),
                ('product_slug', models.SlugField()),
                ('brand', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('stock_quantity', models.CharField(max_length=50)),
                ('sku', models.CharField(blank=True, max_length=50, null=True)),
                ('size', models.CharField(blank=True, max_length=50, null=True)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('weight', models.CharField(blank=True, max_length=50, null=True)),
                ('material', models.CharField(blank=True, max_length=50, null=True)),
                ('width', models.CharField(blank=True, max_length=50, null=True)),
                ('height', models.CharField(blank=True, max_length=50, null=True)),
                ('tags', models.CharField(blank=True, max_length=50, null=True)),
                ('product_pic_front', models.ImageField(upload_to='products/product_photo/')),
                ('product_pic_back', models.ImageField(upload_to='products/product_photo/')),
                ('product_pic_third', models.ImageField(blank=True, null=True, upload_to='products/product_photo/')),
                ('product_pic_fourth', models.ImageField(blank=True, null=True, upload_to='products/product_photo/')),
                ('created_at', models.TimeField(auto_now_add=True)),
                ('updated_at', models.TimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='products.category')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='seller.seller')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'product',
                'ordering': ['product_name'],
            },
        ),
    ]
