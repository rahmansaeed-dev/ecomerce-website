# Generated by Django 4.2.7 on 2024-01-02 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_product_discounted_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='category',
            new_name='quantity',
        ),
    ]
