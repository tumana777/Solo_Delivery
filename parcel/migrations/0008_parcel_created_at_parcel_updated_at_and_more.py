# Generated by Django 5.1.4 on 2024-12-21 18:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0007_alter_parcel_delivery_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='დაემატა'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parcel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='განახლდა'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='delivery_time',
            field=models.DateField(blank=True, null=True, verbose_name='ჩაბარების თარიღი'),
        ),
    ]
