# Generated by Django 5.1.1 on 2024-09-13 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_latitude_alter_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='User',
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='UserProfile',
        ),
    ]