# Generated by Django 4.2.7 on 2024-01-21 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='user',
        ),
    ]
