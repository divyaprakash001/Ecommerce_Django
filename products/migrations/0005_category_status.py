# Generated by Django 5.1.1 on 2024-10-10 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_category_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='status',
            field=models.CharField(default='Active', max_length=10),
        ),
    ]
