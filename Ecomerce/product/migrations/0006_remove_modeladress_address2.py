# Generated by Django 4.2.7 on 2023-12-27 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_modeladress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modeladress',
            name='address2',
        ),
    ]
