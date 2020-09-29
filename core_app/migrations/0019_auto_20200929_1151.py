# Generated by Django 3.1.1 on 2020-09-29 11:51

import core_app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core_app', '0018_auto_20200929_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=100)),
                ('confirm_id', models.BigIntegerField(default=core_app.models.random_id)),
                ('confirmed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='ExtendedUser',
        ),
    ]
