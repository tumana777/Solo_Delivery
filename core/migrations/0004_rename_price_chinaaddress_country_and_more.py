# Generated by Django 5.1.4 on 2024-12-14 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_chinaaddress_price_usaaddress_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chinaaddress',
            old_name='price',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='usaaddress',
            old_name='price',
            new_name='country',
        ),
    ]
