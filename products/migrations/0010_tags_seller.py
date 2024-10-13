# Generated by Django 5.1.1 on 2024-10-13 12:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_product_desc'),
        ('seller', '0007_seller_seller_linkedin_url_seller_seller_youtube_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='seller.seller'),
        ),
    ]
