# Generated by Django 4.1.5 on 2023-01-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0004_alter_goodincart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverytype',
            name='free_delivery',
            field=models.BooleanField(blank=True, choices=[('Доступна', True), ('Недоступна', False)], default=False, null=True, verbose_name='возможность бесплатной доставки'),
        ),
    ]
