# Generated by Django 5.1.1 on 2024-09-16 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_rename_seller_business_name_seller_seller_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='seller_gst_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]