# Generated by Django 5.1.1 on 2024-09-16 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_alter_user_table_alter_userprofile_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_first_name', models.CharField(max_length=50)),
                ('seller_last_name', models.CharField(max_length=50)),
                ('seller_gst_no', models.CharField(max_length=50, unique=True)),
                ('seller_gst_pic', models.ImageField(upload_to='vendor/gst_pic')),
                ('seller_street', models.CharField(blank=True, max_length=100, null=True)),
                ('seller_city', models.CharField(blank=True, max_length=100, null=True)),
                ('seller_district', models.CharField(blank=True, max_length=50, null=True)),
                ('seller_state', models.CharField(blank=True, max_length=50, null=True)),
                ('seller_country', models.CharField(blank=True, max_length=50, null=True)),
                ('seller_pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('seller_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('seller_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('seller_business_name', models.CharField(blank=True, max_length=100, null=True)),
                ('seller_website_url', models.URLField(blank=True, null=True)),
                ('seller_bank_account', models.CharField(blank=True, max_length=50, null=True)),
                ('seller_payment_methods', models.CharField(blank=True, max_length=255, null=True)),
                ('seller_facebook_url', models.URLField(blank=True, null=True)),
                ('seller_twitter_url', models.URLField(blank=True, null=True)),
                ('seller_instagram_url', models.URLField(blank=True, null=True)),
                ('business_hours', models.TextField(blank=True, null=True)),
                ('shipping_methods', models.TextField(blank=True, null=True)),
                ('shipping_regions', models.TextField(blank=True, null=True)),
                ('terms_and_conditions_url', models.URLField(blank=True, null=True)),
                ('privacy_policy_url', models.URLField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='accounts.userprofile')),
            ],
            options={
                'verbose_name': 'Seller',
                'verbose_name_plural': 'Sellers',
                'db_table': 'seller',
                'ordering': ['created_at'],
            },
        ),
    ]