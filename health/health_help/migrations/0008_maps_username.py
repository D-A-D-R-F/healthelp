# Generated by Django 3.2.4 on 2021-09-12 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_help', '0007_maps'),
    ]

    operations = [
        migrations.AddField(
            model_name='maps',
            name='username',
            field=models.CharField(default='', max_length=250),
        ),
    ]
