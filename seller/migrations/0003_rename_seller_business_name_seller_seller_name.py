# Generated by Django 5.1.1 on 2024-09-16 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_remove_seller_seller_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seller',
            old_name='seller_business_name',
            new_name='seller_name',
        ),
    ]
