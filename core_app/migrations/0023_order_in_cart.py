# Generated by Django 3.1.1 on 2020-10-01 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0022_auto_20201001_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='in_cart',
            field=models.BooleanField(default=True),
        ),
    ]
