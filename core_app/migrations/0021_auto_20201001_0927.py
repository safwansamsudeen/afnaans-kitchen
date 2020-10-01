# Generated by Django 3.1.1 on 2020-10-01 09:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0020_customuser_new_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('main_image', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('description', models.TextField()),
                ('veg', models.BooleanField(default=True)),
                ('is_available', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=50)),
                ('long_name', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='PersonInTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('positions', models.TextField()),
                ('main_image', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('description', models.TextField()),
                ('email_address', models.EmailField(max_length=254)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='fooditemmodel',
            name='food_item_type',
        ),
        migrations.DeleteModel(
            name='TeamModel',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='confirm_id',
            field=models.BigIntegerField(),
        ),
        migrations.DeleteModel(
            name='FoodItemModel',
        ),
        migrations.DeleteModel(
            name='FoodTypeModel',
        ),
        migrations.AddField(
            model_name='fooditem',
            name='food_item_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core_app.foodtype'),
        ),
    ]
