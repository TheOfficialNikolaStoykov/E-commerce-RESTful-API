# Generated by Django 5.1 on 2024-09-13 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipping', 'Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], max_length=12),
        ),
    ]
